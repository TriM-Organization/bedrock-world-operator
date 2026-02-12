package block

import (
	"bytes"
	"slices"

	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

const (
	FNV1_32_INIT  uint32 = 0x811C9DC5
	FNV1_PRIME_32 uint32 = 0x01000193
)

// MarshalInternalData marshal map[string]any{key: value} to its NBT represent.
// Note that only the internal results are returned, and the outer ones are not included.
//
// For example, if key is "12" whose bytes is []byte{49, 50}, and value is int32(7),
// then the return result is []byte{3, 2, 0, 49, 50, 7, 0, 0, 0} but not
// []byte{10, 0, 0, 3, 2, 0, 49, 50, 7, 0, 0, 0, 0}.
//
// The explanation of the example:
//   - 3 => The type of value is TAG_Int (3)
//   - 2, 0 => The length of key ("12") is 2 (little endian represent)
//   - 49, 50 => The content of key ("12")
//   - 7, 0, 0, 0 => The little endian represent of value (7)
func MarshalInternalData(key string, value any) []byte {
	buf := bytes.NewBuffer(nil)
	nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian).Encode(map[string]any{key: value})
	return buf.Bytes()[3 : buf.Len()-1]
}

// Fnv1a_32 compute the fnv1a_32 hash of data.
func Fnv1a_32(data []byte) uint32 {
	hash := FNV1_32_INIT
	for _, datum := range data {
		hash ^= uint32(datum)
		hash *= FNV1_PRIME_32
	}
	return hash
}

// ComputeBlockHash compute the hash of block whose name is blockName, and states is blockStates.
// This implement is edited from https://gist.github.com/Alemiz112/504d0f79feac7ef57eda174b668dd345.
func ComputeBlockHash(blockName string, blockStates map[string]any) uint32 {
	b := bytes.NewBuffer(nil)

	if blockName == "minecraft:unknown" || blockName == "unknown" {
		unknownBlockHash := -2
		return uint32(unknownBlockHash)
	}

	keys := make([]string, 0, len(blockStates))
	for k := range blockStates {
		keys = append(keys, k)
	}
	slices.Sort(keys)

	{
		// The header
		b.Write([]byte{10, 0, 0})

		// "name": blockName
		b.Write(MarshalInternalData("name", blockName))

		// "states": blockStates
		b.Write([]byte{10, 6, 0})
		b.WriteString("states")
		// each element in blockStates
		for _, k := range keys {
			b.Write(MarshalInternalData(k, blockStates[k]))
		}
		// TAG_End of blockStates
		b.WriteByte(0)

		// TAG_End of whole map
		b.WriteByte(0)
	}

	return Fnv1a_32(b.Bytes())
}
