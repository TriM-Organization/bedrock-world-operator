package world

import (
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
)

func (b *BedrockWorld) LoadDeltaUpdate(dm define.Dimension, position define.ChunkPos) ([]byte, error) {
	key := world_define.Sum(dm, position, []byte(world_define.KeyDeltaUpdate)...)
	data, err := b.ldb.Get(key, nil)
	if err != nil {
		return nil, err
	}
	return data, nil
}

func (b *BedrockWorld) SaveDeltaUpdate(dm define.Dimension, position define.ChunkPos, payload []byte) error {
	key := world_define.Sum(dm, position, []byte(world_define.KeyDeltaUpdate)...)
	if len(payload) == 0 {
		return b.ldb.Delete(key, nil)
	}
	return b.ldb.Put(key, payload, nil)
}
