package main

import "C"
import (
	"encoding/binary"

	"github.com/TriM-Organization/bedrock-world-operator/chunk"
)

var savedSubChunk = NewSimpleManager[*chunk.SubChunk]()

//export NewSubChunk
func NewSubChunk(blockTableId C.longlong) C.longlong {
	t := savedBlockTable.LoadObject(int(blockTableId))
	if t == nil {
		return -1
	}
	subChunk := chunk.NewSubChunk((*t).AirRuntimeID())
	return C.longlong(savedSubChunk.AddObject(subChunk))
}

//export ReleaseSubChunk
func ReleaseSubChunk(id C.longlong) {
	savedSubChunk.ReleaseObject(int(id))
}

//export SubChunk_Block
func SubChunk_Block(id C.longlong, x C.int, y C.int, z C.int, layer C.int) (blockRuntimeID C.int) {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return -1
	}
	return C.int((*subChunk).Block(byte(x), byte(y), byte(z), uint8(layer)))
}

//export SubChunk_Blocks
func SubChunk_Blocks(id C.longlong, layer C.int) (complexReturn *C.char) {
	c := savedSubChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}

	allBlocks := (*c).Blocks(uint8(layer))
	result := make([]byte, 4096*4)

	ptr := 0
	for _, value := range allBlocks {
		runtimeIDBytes := make([]byte, 4)
		binary.LittleEndian.PutUint32(runtimeIDBytes, value)
		result[ptr], result[ptr+1], result[ptr+2], result[ptr+3] = runtimeIDBytes[0], runtimeIDBytes[1], runtimeIDBytes[2], runtimeIDBytes[3]
		ptr += 4
	}

	return asCbytes(result)
}

//export SubChunk_Empty
func SubChunk_Empty(id C.longlong) C.int {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return -1
	}
	return asCbool((*subChunk).Empty())
}

//export SubChunk_Equals
func SubChunk_Equals(id C.longlong, anotherSubChunkId C.longlong) C.int {
	s1 := savedSubChunk.LoadObject(int(id))
	s2 := savedSubChunk.LoadObject(int(anotherSubChunkId))
	if s1 == nil || s2 == nil {
		return -1
	}
	return asCbool((*s1).Equals(*s2))
}

//export SubChunk_SetBlock
func SubChunk_SetBlock(id C.longlong, x C.int, y C.int, z C.int, layer C.int, block C.int) *C.char {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return C.CString("SubChunk_SetBlock: Sub chunk not found")
	}
	(*subChunk).SetBlock(byte(x), byte(y), byte(z), uint8(layer), uint32(block))
	return C.CString("")
}

//export SubChunk_SetBlocks
func SubChunk_SetBlocks(id C.longlong, layer C.int, payload *C.char) *C.char {
	c := savedSubChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("SubChunk_SetBlocks: Chunk not found")
	}

	goBytes := asGoBytes(payload)
	blocks := make([]uint32, len(goBytes)/4)

	ptr := 0
	for i := range len(blocks) {
		blocks[i] = binary.LittleEndian.Uint32(goBytes[ptr : ptr+4])
		ptr += 4
	}

	(*c).SetBlocks(uint8(layer), blocks)
	return C.CString("")
}
