package world

import (
	"bytes"
	"encoding/binary"

	"github.com/TriM-Organization/bedrock-world-operator/chunk"
	"github.com/TriM-Organization/bedrock-world-operator/define"
	world_define "github.com/TriM-Organization/bedrock-world-operator/world/define"
)

// LoadSubChunk loads a sub chunk at the position from the leveldb database.
func (b *BedrockWorld) LoadSubChunk(dm define.Dimension, position define.SubChunkPos) *chunk.SubChunk {
	chunkPos := define.ChunkPos{position[0], position[2]}
	keyBytes := world_define.Sum(
		dm, chunkPos,
		world_define.KeySubChunkData, byte(position[1]),
	)

	r := define.Dimension(dm).Range()
	if position[1] < int32(r[0]>>4) || position[1] > int32(r[1]>>4) {
		return nil
	}

	subChunkData, _ := b.Get(keyBytes)
	if len(subChunkData) == 0 {
		has, err := b.Has(world_define.Sum(dm, chunkPos, world_define.KeyVersion))
		if err == nil && !has {
			// The new key was not found, so we try the old key.
			has, err = b.Has(world_define.Sum(dm, chunkPos, world_define.KeyVersionOld))
		}
		if err == nil && has {
			return chunk.NewSubChunk(b.blockRuntimeIDTable.AirRuntimeID())
		}
		return nil
	}

	subChunk, _, err := chunk.DecodeSubChunk(
		bytes.NewBuffer(subChunkData),
		dm.Range(),
		chunk.DiskEncoding,
		b.blockRuntimeIDTable,
	)
	if err != nil {
		return nil
	}

	return subChunk
}

// SaveSubChunk saves a sub chunk at the position passed to the leveldb database.
// Its version is written as the version in the chunkVersion constant.
func (b *BedrockWorld) SaveSubChunk(dm define.Dimension, position define.SubChunkPos, c *chunk.SubChunk) error {
	chunkPos := define.ChunkPos{position[0], position[2]}
	subChunkKey := world_define.Sum(dm, chunkPos, world_define.KeySubChunkData, byte(position[1]))
	if c == nil {
		return b.Delete(subChunkKey)
	}

	finalisation := make([]byte, 4)
	binary.LittleEndian.PutUint32(finalisation, world_define.FinalisationGenerated)
	_ = b.Put(
		world_define.Sum(dm, chunkPos, world_define.KeyVersion),
		[]byte{world_define.ChunkVersion},
	)
	_ = b.Put(
		world_define.Sum(dm, chunkPos, world_define.KeyFinalisation),
		finalisation,
	)

	fixedYPos := (position[1]<<4 - int32(dm.Range()[0])) >> 4
	subChunkData := chunk.EncodeSubChunk(c, dm.Range(), int(fixedYPos), chunk.DiskEncoding, b.blockRuntimeIDTable)
	return b.Put(subChunkKey, subChunkData)
}
