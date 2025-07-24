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

	subChunkData, _ := b.Get(
		world_define.Sum(
			dm, chunkPos,
			world_define.KeySubChunkData, byte(position[1]),
		),
	)
	if len(subChunkData) == 0 {
		return nil
	}

	subChunk, _, err := chunk.DecodeSubChunk(bytes.NewBuffer(subChunkData), dm.Range(), chunk.DiskEncoding)
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
	subChunkData := chunk.EncodeSubChunk(c, dm.Range(), int(fixedYPos), chunk.DiskEncoding)
	return b.Put(subChunkKey, subChunkData)
}
