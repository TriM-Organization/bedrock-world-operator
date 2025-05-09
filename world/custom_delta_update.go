package world

import (
	"github.com/TriM-Organization/bedrock-world-operator/define"
	world_define "github.com/TriM-Organization/bedrock-world-operator/world/define"
)

func (b *BedrockWorld) LoadDeltaUpdate(dm define.Dimension, position define.ChunkPos) ([]byte, error) {
	key := world_define.Sum(dm, position, []byte(world_define.KeyDeltaUpdate)...)
	data, err := b.Get(key)
	if err != nil {
		return nil, err
	}
	return data, nil
}

func (b *BedrockWorld) SaveDeltaUpdate(dm define.Dimension, position define.ChunkPos, payload []byte) error {
	key := world_define.Sum(dm, position, []byte(world_define.KeyDeltaUpdate)...)
	if len(payload) == 0 {
		return b.Delete(key)
	}
	return b.Put(key, payload)
}
