package world

import (
	"bytes"
	"fmt"
	"strings"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	world_define "github.com/YingLunTown-DreamLand/bedrock-world-operator/world/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

// LoadNBTPayloadOnly loads payload of all block entities from the chunk position passed.
func (b *BedrockWorld) LoadNBTPayloadOnly(dm define.Dimension, position define.ChunkPos) []byte {
	key := world_define.Sum(dm, position, world_define.KeyBlockEntities)
	data, err := b.Get(key)
	if err != nil {
		return nil
	}
	return data
}

// LoadNBT loads all block entities from the chunk position passed.
func (b *BedrockWorld) LoadNBT(dm define.Dimension, position define.ChunkPos) ([]map[string]any, error) {
	data := b.LoadNBTPayloadOnly(dm, position)
	if len(data) == 0 {
		return make([]map[string]any, 0), nil
	}

	var a []map[string]any
	buf := bytes.NewBuffer(data)
	dec := nbt.NewDecoderWithEncoding(buf, nbt.LittleEndian)

	for buf.Len() != 0 {
		var m map[string]any
		if err := dec.Decode(&m); err != nil {
			return nil, fmt.Errorf("error decoding block NBT: %w", err)
		}
		if _id, found := m["id"]; found {
			if id, ok := _id.(string); ok {
				if strings.HasPrefix(id, "minecraft:") {
					id = strings.TrimPrefix(id, "minecraft:")
					if len(id) > 0 {
						id = strings.ToUpper(string(id[0])) + id[1:]
					}
				}
				m["id"] = id
			}
		}
		a = append(a, m)
	}
	return a, nil
}

// SaveNBTPayloadOnly saves a serialized NBT data to the chunk position passed.
func (b *BedrockWorld) SaveNBTPayloadOnly(dm define.Dimension, position define.ChunkPos, data []byte) error {
	key := world_define.Sum(dm, position, world_define.KeyBlockEntities)
	if len(data) == 0 {
		return b.Delete(key)
	}
	return b.Put(key, data)
}

// SaveNBT saves all block NBT data to the chunk position passed.
func (b *BedrockWorld) SaveNBT(dm define.Dimension, position define.ChunkPos, data []map[string]any) error {
	buf := bytes.NewBuffer(nil)
	enc := nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian)
	for _, d := range data {
		if err := enc.Encode(d); err != nil {
			return fmt.Errorf("error encoding block NBT: %w", err)
		}
	}
	return b.SaveNBTPayloadOnly(dm, position, buf.Bytes())
}
