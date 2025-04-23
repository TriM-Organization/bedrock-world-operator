package main

import "C"
import (
	"bytes"
	"encoding/binary"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/block"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/chunk"
)

var savedChunk = NewSimpleManager[*chunk.Chunk]()

//export NewChunk
func NewChunk(rangeStart C.int, rangeEnd C.int) C.int {
	c := chunk.NewChunk(block.AirRuntimeID, [2]int{int(rangeStart), int(rangeEnd)})
	return C.int(savedChunk.AddObject(c))
}

//export ReleaseChunk
func ReleaseChunk(id C.int) {
	savedChunk.ReleaseObject(int(id))
}

//export Chunk_Biome
func Chunk_Biome(id C.int, x C.int, y C.int, z C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).Biome(uint8(x), int16(y), uint8(z)))
}

//export Chunk_Block
func Chunk_Block(id C.int, x C.int, y C.int, z C.int, layer C.int) (blockRuntimeID C.int) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	(*c).Range()
	return C.int((*c).Block(uint8(x), int16(y), uint8(z), uint8(layer)))
}

//export Chunk_Blocks
func Chunk_Blocks(id C.int, layer C.int) (complexReturn *C.char) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}

	allBlocks := (*c).Blocks(uint8(layer))
	result := make([]byte, 4096*len(allBlocks)*4)

	ptr := 0
	for _, value := range allBlocks {
		for _, v := range value {
			runtimeIDBytes := make([]byte, 4)
			binary.LittleEndian.PutUint32(runtimeIDBytes, v)
			result[ptr], result[ptr+1], result[ptr+2], result[ptr+3] = runtimeIDBytes[0], runtimeIDBytes[1], runtimeIDBytes[2], runtimeIDBytes[3]
			ptr += 4
		}
	}

	return asCbytes(result)
}

//export Chunk_Compact
func Chunk_Compact(id C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_Compact: Chunk not found")
	}
	(*c).Compact()
	return C.CString("")
}

//export Chunk_Equals
func Chunk_Equals(id C.int, anotherChunkID C.int) C.int {
	c1 := savedChunk.LoadObject(int(id))
	c2 := savedChunk.LoadObject(int(anotherChunkID))
	if c1 == nil || c2 == nil {
		return -1
	}
	return asCbool((*c1).Equals(*c2))
}

//export Chunk_HighestFilledSubChunk
func Chunk_HighestFilledSubChunk(id C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).HighestFilledSubChunk())
}

//export Chunk_Range
func Chunk_Range(id C.int) (rangeBytes *C.char) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}

	result := make([]byte, 8)
	r := (*c).Range()
	binary.LittleEndian.PutUint32(result, uint32(r[0]))
	binary.LittleEndian.PutUint32(result[4:], uint32(r[1]))

	return asCbytes(result)
}

//export Chunk_SetBiome
func Chunk_SetBiome(id C.int, x C.int, y C.int, z C.int, biomeId C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBiome: Chunk not found")
	}
	(*c).SetBiome(uint8(x), int16(y), uint8(z), uint32(biomeId))
	return C.CString("")
}

//export Chunk_SetBlock
func Chunk_SetBlock(id C.int, x C.int, y C.int, z C.int, layer C.int, block C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBlock: Chunk not found")
	}
	(*c).SetBlock(uint8(x), int16(y), uint8(z), uint8(layer), uint32(block))
	return C.CString("")
}

//export Chunk_SetBlocks
func Chunk_SetBlocks(id C.int, layer C.int, payload *C.char) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBlock: Chunk not found")
	}

	goBytes := asGoBytes(payload)
	blocks := make([][]uint32, len(goBytes)/4/4096)

	ptr := 0
	for i := range len(blocks) {
		blocks[i] = make([]uint32, 4096)
		for j := range 4096 {
			blocks[i][j] = binary.LittleEndian.Uint32(goBytes[ptr : ptr+4])
			ptr += 4
		}
	}

	(*c).SetBlocks(uint8(layer), blocks)
	return C.CString("")
}

//export Chunk_Sub
func Chunk_Sub(id C.int) (complexReturn *C.char) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}

	sub := (*c).Sub()
	linkedId := make([]int, len(sub))
	for index, value := range sub {
		linkedId[index] = savedSubChunk.AddObject(value)
	}

	buf := bytes.NewBuffer(nil)
	for _, value := range linkedId {
		temp := make([]byte, 4)
		binary.LittleEndian.PutUint32(temp, uint32(value))
		_, _ = buf.Write(temp)
	}

	return asCbytes(buf.Bytes())
}

//export Chunk_SubChunk
func Chunk_SubChunk(id C.int, y C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int(savedSubChunk.AddObject((*c).SubChunk(int16(y))))
}

//export Chunk_SubIndex
func Chunk_SubIndex(id C.int, y C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).SubIndex(int16(y)))
}

//export Chunk_SubY
func Chunk_SubY(id C.int, index C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).SubY(int16(index)))
}
