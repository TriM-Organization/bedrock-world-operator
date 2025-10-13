package main

import "C"
import (
	"github.com/TriM-Organization/bedrock-world-operator/chunk"
)

//export SubChunkNetworkPayload
func SubChunkNetworkPayload(subChunkId C.longlong, blockTableId C.longlong, rangeStart C.int, rangeEnd C.int, ind C.int) *C.char {
	return subChunkPayload(subChunkId, blockTableId, rangeStart, rangeEnd, ind, chunk.NetworkEncoding)
}

//export FromSubChunkNetworkPayload
func FromSubChunkNetworkPayload(blockTableId C.longlong, rangeStart C.int, rangeEnd C.int, payload *C.char) (complexReturn *C.char) {
	return fromSubChunkPayload(blockTableId, rangeStart, rangeEnd, payload, chunk.NetworkEncoding)
}

//export SubChunkDiskPayload
func SubChunkDiskPayload(subChunkId C.longlong, blockTableId C.longlong, rangeStart C.int, rangeEnd C.int, ind C.int) *C.char {
	return subChunkPayload(subChunkId, blockTableId, rangeStart, rangeEnd, ind, chunk.DiskEncoding)
}

//export FromSubChunkDiskPayload
func FromSubChunkDiskPayload(blockTableId C.longlong, rangeStart C.int, rangeEnd C.int, payload *C.char) (complexReturn *C.char) {
	return fromSubChunkPayload(blockTableId, rangeStart, rangeEnd, payload, chunk.DiskEncoding)
}
