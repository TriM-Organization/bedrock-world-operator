package world

import (
	"encoding/binary"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
)

// LoadFullSubChunkBlobHash load the blob hash of a chunk.
func (b *BedrockWorld) LoadFullSubChunkBlobHash(dm define.Dimension, position define.ChunkPos) (result []define.HashWithPosY) {
	result = make([]define.HashWithPosY, 0)

	key := world_define.Sum(dm, position, []byte(world_define.KeyBlobHash)...)
	data, err := b.Get(key)
	if err != nil || len(data) == 0 {
		return nil
	}

	// SubChunkPos.Y(), Blob hash
	//		 	  int8,	   uint64
	for len(data) > 0 {
		result = append(result, define.HashWithPosY{
			Hash: binary.LittleEndian.Uint64(data[1:9]),
			PosY: int8(data[0]),
		})
		data = data[9:]
	}

	return result
}

// LoadSubChunkBlobHash load the blob hash of a
// sub chunk that in position and in dm dimension.
func (b *BedrockWorld) LoadSubChunkBlobHash(dm define.Dimension, position define.SubChunkPos) (hash uint64, found bool) {
	key := world_define.Sum(dm, define.ChunkPos{position[0], position[2]}, []byte(world_define.KeyBlobHash)...)
	data, err := b.Get(key)
	if err != nil || len(data) == 0 {
		return 0, false
	}

	// SubChunkPos.Y(), Blob hash
	//		 	  int8,	   uint64
	for len(data) > 0 {
		if int8(data[0]) == int8(position[1]) {
			return binary.LittleEndian.Uint64(data[1:9]), true
		}
		data = data[9:]
	}

	return 0, false
}

// SaveFullSubChunkBlobHash update the blob hash of a chunk.
//
// Note that:
//   - If len(newHash) is 0, then the blob hash
//     data of this chunk will be delete.
//   - Zero hash is allowed.
func (b *BedrockWorld) SaveFullSubChunkBlobHash(dm define.Dimension, position define.ChunkPos, newHash []define.HashWithPosY) error {
	key := world_define.Sum(dm, position, []byte(world_define.KeyBlobHash)...)
	data := make([]byte, 0)

	// SubChunkPos.Y(), Blob hash
	//		 	  int8,	   uint64
	for _, value := range newHash {
		hashBytes := make([]byte, 8)
		binary.LittleEndian.PutUint64(hashBytes, uint64(value.Hash))
		data = append(data, uint8(value.PosY))
		data = append(data, hashBytes...)
	}

	if len(data) == 0 {
		return b.Delete(key)
	} else {
		return b.Put(key, data)
	}
}

// SaveSubChunkBlobHash save the hash for sub chunk
// which in position and in dm dimension.
// Note that zero hash is allowed.
func (b *BedrockWorld) SaveSubChunkBlobHash(dm define.Dimension, position define.SubChunkPos, hash uint64) error {
	diskHasHash := false
	modified := make([]byte, 0)

	hashByte := make([]byte, 8)
	binary.LittleEndian.PutUint64(hashByte, hash)

	key := world_define.Sum(dm, define.ChunkPos{position[0], position[2]}, []byte(world_define.KeyBlobHash)...)
	data, err := b.Get(key)

	if err == nil && len(data) != 0 {
		// SubChunkPos.Y(), Blob hash
		//		 	  int8,	   uint64
		for len(data) > 0 {
			if int8(data[0]) == int8(position[1]) {
				modified = append(modified, data[0])
				modified = append(modified, hashByte...)
				diskHasHash = true
			} else {
				modified = append(modified, data[0:9]...)
			}
			data = data[9:]
		}
	}

	if !diskHasHash {
		modified = append(modified, uint8(position[1]))
		modified = append(modified, hashByte...)
	}

	if len(modified) == 0 {
		return b.Delete(key)
	} else {
		return b.Put(key, modified)
	}
}
