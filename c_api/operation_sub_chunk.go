package main

import "C"
import (
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/block"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/chunk"
)

var savedSubChunk = NewSimpleManager[*chunk.SubChunk]()

//export NewSubChunk
func NewSubChunk(rangeStart C.int, rangeEnd C.int) C.int {
	subChunk := chunk.NewSubChunk(block.AirRuntimeID)
	return C.int(savedSubChunk.AddObject(subChunk))
}

//export ReleaseSubChunk
func ReleaseSubChunk(id C.int) {
	savedSubChunk.ReleaseObject(int(id))
}

//export SubChunk_Block
func SubChunk_Block(id C.int, x C.int, y C.int, z C.int, layer C.int) (blockRuntimeID C.int) {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return -1
	}
	return C.int((*subChunk).Block(byte(x), byte(y), byte(z), uint8(layer)))
}

//export SubChunk_Empty
func SubChunk_Empty(id C.int) C.int {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return -1
	}
	return asCbool((*subChunk).Empty())
}

//export SubChunk_Equals
func SubChunk_Equals(id C.int, anotherSubChunkId C.int) C.int {
	s1 := savedSubChunk.LoadObject(int(id))
	s2 := savedSubChunk.LoadObject(int(anotherSubChunkId))
	if s1 == nil || s2 == nil {
		return -1
	}
	return asCbool((*s1).Equals(*s2))
}

//export SubChunk_SetBlock
func SubChunk_SetBlock(id C.int, x C.int, y C.int, z C.int, layer C.int, block C.int) {
	subChunk := savedSubChunk.LoadObject(int(id))
	if subChunk == nil {
		return
	}
	(*subChunk).SetBlock(byte(x), byte(y), byte(z), uint8(layer), uint32(block))
}
