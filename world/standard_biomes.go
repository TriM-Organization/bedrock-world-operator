package world

import (
	"fmt"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
)

func (b *BedrockWorld) LoadBiomes(dm define.Dimension, position define.ChunkPos) ([]byte, error) {
	biomes, err := b.Get(world_define.Sum(dm, position, world_define.Key3DData))
	if err != nil {
		return nil, err
	}
	// The first 512 bytes is a heightmap (16*16 int16s), the biomes follow. We
	// calculate a heightmap on startup so the heightmap can be discarded.
	if n := len(biomes); n <= 512 {
		return nil, fmt.Errorf("expected at least 512 bytes for 3D data, got %v", n)
	}
	return biomes[512:], nil
}

func (b *BedrockWorld) SaveBiomes(dm define.Dimension, position define.ChunkPos, payload []byte) error {
	key := world_define.Sum(dm, position, world_define.Key3DData)
	if len(payload) == 0 {
		return b.Delete(key)
	}
	return b.Put(key, append(make([]byte, 512), payload...))
}
