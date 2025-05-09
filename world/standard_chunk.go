package world

import (
	"encoding/binary"
	"fmt"

	"github.com/TriM-Organization/bedrock-world-operator/chunk"
	"github.com/TriM-Organization/bedrock-world-operator/define"
	world_define "github.com/TriM-Organization/bedrock-world-operator/world/define"
)

// LoadChunkPayloadOnly loads a chunk at the position passed from the leveldb database.
// If it doesn't exist, exists is false.
// If an error is returned, exists is always assumed to be true.
// Note that we here don't decode chunk data and just return the origin payload.
func (b *BedrockWorld) LoadChunkPayloadOnly(dm define.Dimension, position define.ChunkPos) (subchunksBytes [][]byte, exists bool, err error) {
	subchunksBytes = make([][]byte, dm.Height()>>4)
	// This key is where the version of a chunk resides. The chunk version has changed many times, without any
	// actual substantial changes, so we don't check this.

	data, err := b.Get(world_define.Sum(dm, position, world_define.KeyVersion))

	if data == nil && err == nil {
		// The new key was not found, so we try the old key.
		data, err = b.Get(world_define.Sum(dm, position, world_define.KeyVersionOld))
		if data == nil && err == nil {
			return nil, false, nil
		}
	} else if err != nil {
		return nil, true, fmt.Errorf("error reading version: %w", err)
	}

	for i := range subchunksBytes {
		subchunksBytes[i], err = b.Get(
			world_define.Sum(
				dm, position,
				world_define.KeySubChunkData, uint8(i+(dm.Range()[0]>>4)),
			),
		)
		if subchunksBytes[i] == nil && err == nil {
			// No sub chunk present at this Y level. We skip this one and move to the next, which might still
			// be present.
			continue
		} else if err != nil {
			return nil, true, fmt.Errorf("error reading sub chunk data %v: %w", i, err)
		}
	}

	return subchunksBytes, true, err
}

// LoadChunk loads a chunk at the position passed from the leveldb database. If it doesn't exist, exists is
// false. If an error is returned, exists is always assumed to be true.
func (b *BedrockWorld) LoadChunk(dm define.Dimension, position define.ChunkPos) (c *chunk.Chunk, exists bool, err error) {
	subchunksBytes, exists, err := b.LoadChunkPayloadOnly(dm, position)
	if !exists || err != nil {
		return nil, exists, err
	}

	biomes, err := b.LoadBiomes(dm, position)
	if err != nil {
		biomes = make([]byte, 0)
	}

	c, err = chunk.DiskDecode(
		chunk.SerialisedData{
			SubChunks: subchunksBytes,
			Biomes:    biomes,
		},
		dm.Range(),
	)
	return c, true, err
}

// SaveChunkPayloadOnly saves a serialized chunk at the position passed to the leveldb database.
// Its version is written as the version in the chunkVersion constant.
func (b *BedrockWorld) SaveChunkPayloadOnly(dm define.Dimension, position define.ChunkPos, subchunksBytes [][]byte) error {
	_ = b.Put(
		world_define.Sum(dm, position, world_define.KeyVersion),
		[]byte{world_define.ChunkVersion},
	)

	finalisation := make([]byte, 4)
	binary.LittleEndian.PutUint32(finalisation, world_define.FinalisationPopulated)
	_ = b.Put(
		world_define.Sum(dm, position, world_define.KeyFinalisation),
		finalisation,
	)

	for i, sub := range subchunksBytes {
		if len(sub) == 0 {
			_ = b.Delete(
				world_define.Sum(
					dm, position,
					world_define.KeySubChunkData, byte(i+(dm.Range()[0]>>4)),
				),
			)
			continue
		}
		_ = b.Put(
			world_define.Sum(
				dm, position,
				world_define.KeySubChunkData, byte(i+(dm.Range()[0]>>4)),
			),
			sub,
		)
	}
	return nil
}

// SaveChunk saves a chunk at the position passed to the leveldb database. Its version is written as the
// version in the chunkVersion constant.
func (b *BedrockWorld) SaveChunk(dm define.Dimension, position define.ChunkPos, c *chunk.Chunk) error {
	if c == nil {
		return nil
	}
	serialisedData := chunk.Encode(c, chunk.DiskEncoding)

	err := b.SaveBiomes(dm, position, serialisedData.Biomes)
	if err != nil {
		return fmt.Errorf("SaveChunk: %v", err)
	}

	err = b.SaveChunkPayloadOnly(dm, position, serialisedData.SubChunks)
	if err != nil {
		return fmt.Errorf("SaveChunk: %v", err)
	}

	return nil
}
