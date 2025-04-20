package world

import (
	"encoding/binary"
	"fmt"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/chunk"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
	"github.com/df-mc/goleveldb/leveldb"
)

// LoadChunkPayloadOnly loads a chunk at the position passed from the leveldb database.
// If it doesn't exist, exists is false.
// If an error is returned, exists is always assumed to be true.
// Note that we here don't decode chunk data and just return the origin payload.
func (b *BedrockWorld) LoadChunkPayloadOnly(dm define.Dimension, position define.ChunkPos) (subchunksBytes [][]byte, exists bool, err error) {
	subchunksBytes = make([][]byte, (dm.Height()>>4)+1)
	// This key is where the version of a chunk resides. The chunk version has changed many times, without any
	// actual substantial changes, so we don't check this.
	_, err = b.ldb.Get(world_define.Sum(dm, position, world_define.KeyVersion), nil)
	if err == leveldb.ErrNotFound {
		// The new key was not found, so we try the old key.
		if _, err = b.ldb.Get(world_define.Sum(dm, position, world_define.KeyVersionOld), nil); err != nil {
			return nil, false, nil
		}
	} else if err != nil {
		return nil, true, fmt.Errorf("error reading version: %w", err)
	}
	for i := range subchunksBytes {
		subchunksBytes[i], err = b.ldb.Get(
			world_define.Sum(
				dm, position,
				world_define.KeySubChunkData, uint8(i+(dm.Range()[0]>>4)),
			),
			nil,
		)
		if err == leveldb.ErrNotFound {
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
	_ = b.ldb.Put(
		world_define.Sum(dm, position, world_define.KeyVersion),
		[]byte{world_define.ChunkVersion},
		nil,
	)

	finalisation := make([]byte, 4)
	binary.LittleEndian.PutUint32(finalisation, world_define.FinalisationPopulated)
	_ = b.ldb.Put(
		world_define.Sum(dm, position, world_define.KeyFinalisation),
		finalisation,
		nil,
	)

	for i, sub := range subchunksBytes {
		if len(sub) == 0 {
			_ = b.ldb.Delete(
				world_define.Sum(
					dm, position,
					world_define.KeySubChunkData, byte(i+(dm.Range()[0]>>4)),
				),
				nil,
			)
			continue
		}
		_ = b.ldb.Put(
			world_define.Sum(
				dm, position,
				world_define.KeySubChunkData, byte(i+(dm.Range()[0]>>4)),
			),
			sub,
			nil,
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
