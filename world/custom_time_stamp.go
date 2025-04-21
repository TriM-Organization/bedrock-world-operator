package world

import (
	"encoding/binary"
	"time"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
)

var TimeStampNotFound = time.Unix(0, 0).Unix()

func (b *BedrockWorld) loadTimeStampByKey(dm define.Dimension, position define.ChunkPos, key ...byte) (timeStamp int64) {
	keyBytes := world_define.Sum(dm, position, key...)
	data, err := b.Get(keyBytes)
	if err != nil || len(data) == 0 {
		return TimeStampNotFound
	}
	return int64(binary.LittleEndian.Uint64(data))
}

func (b *BedrockWorld) LoadDeltaUpdateTimeStamp(dm define.Dimension, position define.ChunkPos) (timeStamp int64) {
	return b.loadTimeStampByKey(dm, position, []byte(world_define.KeyDeltaUpdateTimeStamp)...)
}

func (b *BedrockWorld) LoadTimeStamp(dm define.Dimension, position define.ChunkPos) (timeStamp int64) {
	return b.loadTimeStampByKey(dm, position, world_define.KeyChunkTimeStamp)
}

func (b *BedrockWorld) saveTimeStampByKey(dm define.Dimension, position define.ChunkPos, timeStamp int64, key ...byte) error {
	keyBytes := world_define.Sum(dm, position, key...)
	if timeStamp == 0 {
		return b.Delete(keyBytes)
	}
	timeStampBytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(timeStampBytes, uint64(timeStamp))
	return b.Put(keyBytes, timeStampBytes)
}

func (b *BedrockWorld) SaveTimeStamp(dm define.Dimension, position define.ChunkPos, timeStamp int64) error {
	return b.saveTimeStampByKey(dm, position, timeStamp, world_define.KeyChunkTimeStamp)
}

func (b *BedrockWorld) SaveDeltaUpdateTimeStamp(dm define.Dimension, position define.ChunkPos, timeStamp int64) error {
	return b.saveTimeStampByKey(dm, position, timeStamp, []byte(world_define.KeyDeltaUpdateTimeStamp)...)
}
