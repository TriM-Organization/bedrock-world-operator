package main

import "C"
import (
	"bytes"
	"encoding/binary"
	"fmt"

	"github.com/TriM-Organization/bedrock-world-operator/chunk"
	"github.com/TriM-Organization/bedrock-world-operator/define"
)

var savedChunk = NewSimpleManager[*chunk.Chunk]()

//export NewChunk
func NewChunk(blockTableId C.longlong, rangeStart C.int, rangeEnd C.int) (complexReturn *C.char) {
	t := savedBlockTable.LoadObject(int(blockTableId))
	if t == nil {
		return asCbytes(nil)
	}
	c := chunk.NewChunk(
		(*t).AirRuntimeID(),
		define.Range{int(rangeStart), int(rangeEnd)},
	)
	return packChunkRangeAndID(c.Range(), savedChunk.AddObject(c))
}

//export ReleaseChunk
func ReleaseChunk(id C.longlong) {
	savedChunk.ReleaseObject(int(id))
}

//export Chunk_Biome
func Chunk_Biome(id C.longlong, x C.int, y C.int, z C.int) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).Biome(uint8(x), int16(y), uint8(z)))
}

//export Chunk_Biomes
func Chunk_Biomes(id C.longlong) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}
	return asCbytes(packDenseBlockMatrix((*c).Biomes(), 4096))
}

//export Chunk_Block
func Chunk_Block(id C.longlong, x C.int, y C.int, z C.int, layer C.int) (blockRuntimeID C.int) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	(*c).Range()
	return C.int((*c).Block(uint8(x), int16(y), uint8(z), uint8(layer)))
}

//export Chunk_Blocks
func Chunk_Blocks(id C.longlong, layer C.int) (complexReturn *C.char) {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return asCbytes(nil)
	}
	return asCbytes(packDenseBlockMatrix((*c).Blocks(uint8(layer)), 4096))
}

//export Chunk_Compact
func Chunk_Compact(id C.longlong) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_Compact: Chunk not found")
	}
	(*c).Compact()
	return C.CString("")
}

//export Chunk_Equals
func Chunk_Equals(id C.longlong, anotherChunkID C.longlong) C.int {
	c1 := savedChunk.LoadObject(int(id))
	c2 := savedChunk.LoadObject(int(anotherChunkID))
	if c1 == nil || c2 == nil {
		return -1
	}
	return asCbool((*c1).Equals(*c2))
}

//export Chunk_HighestFilledSubChunk
func Chunk_HighestFilledSubChunk(id C.longlong) C.int {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.int((*c).HighestFilledSubChunk())
}

//export Chunk_SetBiome
func Chunk_SetBiome(id C.longlong, x C.int, y C.int, z C.int, biomeId C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBiome: Chunk not found")
	}
	(*c).SetBiome(uint8(x), int16(y), uint8(z), uint32(biomeId))
	return C.CString("")
}

//export Chunk_SetBiomes
func Chunk_SetBiomes(id C.longlong, payload *C.char) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBiomes: Chunk not found")
	}
	(*c).SetBiomes(unpackDenseBlockMatrix(asGoBytes(payload), 4096))
	return C.CString("")
}

//export Chunk_SetBlock
func Chunk_SetBlock(id C.longlong, x C.int, y C.int, z C.int, layer C.int, block C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBlock: Chunk not found")
	}
	(*c).SetBlock(uint8(x), int16(y), uint8(z), uint8(layer), uint32(block))
	return C.CString("")
}

//export Chunk_SetBlocks
func Chunk_SetBlocks(id C.longlong, layer C.int, payload *C.char) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetBlock: Chunk not found")
	}
	(*c).SetBlocks(uint8(layer), unpackDenseBlockMatrix(asGoBytes(payload), 4096))
	return C.CString("")
}

//export Chunk_Sub
func Chunk_Sub(id C.longlong) (complexReturn *C.char) {
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
		temp := make([]byte, 8)
		binary.LittleEndian.PutUint64(temp, uint64(value))
		_, _ = buf.Write(temp)
	}

	return asCbytes(buf.Bytes())
}

//export Chunk_SetSub
func Chunk_SetSub(id C.longlong, linkedIdBytes *C.char) *C.char {
	linkedId := make([]int, 0)
	subChunks := make([]*chunk.SubChunk, 0)

	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetSub: Chunk not found")
	}

	goBytes := asGoBytes(linkedIdBytes)
	for len(goBytes) > 0 {
		linkedId = append(linkedId, int(binary.LittleEndian.Uint64(goBytes)))
		goBytes = goBytes[8:]
	}

	for index, value := range linkedId {
		s := savedSubChunk.LoadObject(value)
		if s == nil {
			return C.CString(fmt.Sprintf("Chunk_SetSub: Sub chunk whose index is %d (id=%d) was not found", index, value))
		}
		subChunks = append(subChunks, *s)
	}

	(*c).SetSub(subChunks)
	return C.CString("")
}

//export Chunk_SubChunk
func Chunk_SubChunk(id C.longlong, y C.int) C.longlong {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return -1
	}
	return C.longlong(savedSubChunk.AddObject((*c).SubChunk(int16(y))))
}

//export Chunk_SetSubChunk
func Chunk_SetSubChunk(id C.longlong, subChunkId C.longlong, index C.int) *C.char {
	c := savedChunk.LoadObject(int(id))
	if c == nil {
		return C.CString("Chunk_SetSubChunk: Chunk not found")
	}

	s := savedSubChunk.LoadObject(int(subChunkId))
	if s == nil {
		return C.CString("Chunk_SetSubChunk: Chunk found but sub chunk not found")
	}

	(*c).SetSubChunk(*s, int16(index))
	return C.CString("")
}
