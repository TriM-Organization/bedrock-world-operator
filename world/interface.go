package world

import (
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/chunk"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/world/leveldat"
)

// StandardBedrockWorld is the function that
// bedrock world implements, but only for standard
// minecraft.
type StandardBedrockWorld interface {
	LevelDat() *leveldat.Data
	UpdateLevelDat() error

	LoadBiomes(dm define.Dimension, position define.ChunkPos) ([]byte, error)
	SaveBiomes(dm define.Dimension, position define.ChunkPos, payload []byte) error

	LoadChunkPayloadOnly(dm define.Dimension, position define.ChunkPos) (subchunksBytes [][]byte, exists bool, err error)
	LoadChunk(dm define.Dimension, position define.ChunkPos) (c *chunk.Chunk, exists bool, err error)
	SaveChunkPayloadOnly(dm define.Dimension, position define.ChunkPos, subchunksBytes [][]byte) error
	SaveChunk(dm define.Dimension, position define.ChunkPos, c *chunk.Chunk) error

	LoadSubChunk(dm define.Dimension, position define.SubChunkPos) *chunk.SubChunk
	SaveSubChunk(dm define.Dimension, position define.SubChunkPos, c *chunk.SubChunk) error

	LoadNBTPayloadOnly(dm define.Dimension, position define.ChunkPos) []byte
	LoadNBT(dm define.Dimension, position define.ChunkPos) ([]map[string]any, error)
	SaveNBTPayloadOnly(dm define.Dimension, position define.ChunkPos, data []byte) error
	SaveNBT(dm define.Dimension, position define.ChunkPos, data []map[string]any) error
}

// CustomBedrockWorld is the function that
// bedrock world implements, but for custom
// used purpose, and are not minecraft standard.
type CustomBedrockWorld interface {
	LoadDeltaUpdate(dm define.Dimension, position define.ChunkPos) ([]byte, error)
	SaveDeltaUpdate(dm define.Dimension, position define.ChunkPos, payload []byte) error

	LoadTimeStamp(dm define.Dimension, position define.ChunkPos) (timeStamp int64)
	SaveTimeStamp(dm define.Dimension, position define.ChunkPos, timeStamp int64) error
	LoadDeltaUpdateTimeStamp(dm define.Dimension, position define.ChunkPos) (timeStamp int64)
	SaveDeltaUpdateTimeStamp(dm define.Dimension, position define.ChunkPos, timeStamp int64) error

	LoadFullSubChunkBlobHash(dm define.Dimension, position define.ChunkPos) (result []define.HashWithPosY)
	SaveFullSubChunkBlobHash(dm define.Dimension, position define.ChunkPos, newHash []define.HashWithPosY) error
	LoadSubChunkBlobHash(dm define.Dimension, position define.SubChunkPos) (hash uint64, found bool)
	SaveSubChunkBlobHash(dm define.Dimension, position define.SubChunkPos, hash uint64) error
}

// World is a interface that implements
// standard bedrock world and some custom
// features.
type World interface {
	StandardBedrockWorld
	CustomBedrockWorld
	Close() error
}
