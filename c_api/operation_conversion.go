package main

import "C"
import (
	"bytes"
	"encoding/binary"
	"strings"

	"github.com/Happy2018new/worldupgrader/blockupgrader"
	"github.com/TriM-Organization/bedrock-world-operator/block"
	"github.com/TriM-Organization/bedrock-world-operator/chunk"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

//export RuntimeIDToState
func RuntimeIDToState(runtimeID C.int) (complexReturn *C.char) {
	result := make([]byte, 0)

	name, states, found := block.RuntimeIDToState(uint32(runtimeID))
	if !found {
		// not found
		result = append(result, 0)
		return asCbytes(result)
	}

	// found
	result = append(result, 1)

	// name
	nameLength := make([]byte, 2)
	binary.LittleEndian.PutUint16(nameLength, uint16(len(name)))
	result = append(result, nameLength...)
	result = append(result, []byte(name)...)

	// nbt
	buf := bytes.NewBuffer(nil)
	nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian).Encode(states)
	nbtLength := make([]byte, 4)
	binary.LittleEndian.PutUint32(nbtLength, uint32(buf.Len()))
	result = append(result, nbtLength...)
	result = append(result, buf.Bytes()...)

	return asCbytes(result)
}

//export StateToRuntimeID
func StateToRuntimeID(name *C.char, states *C.char) (complexReturn *C.char) {
	var blockStates map[string]any
	result := make([]byte, 0)

	blockName := C.GoString(name)
	err := nbt.NewDecoderWithEncoding(bytes.NewBuffer(asGoBytes(states)), nbt.LittleEndian).Decode(&blockStates)
	if err != nil {
		// not found
		result = append(result, 0)
		return asCbytes(result)
	}

	if !strings.HasPrefix(blockName, "minecraft:") {
		blockName = "minecraft:" + blockName
	}
	upgraded := blockupgrader.Upgrade(blockupgrader.BlockState{
		Name:       blockName,
		Properties: blockStates,
	})
	runtimeID, found := block.StateToRuntimeID(upgraded.Name, upgraded.Properties)
	if !found {
		// not found
		result = append(result, 0)
		return asCbytes(result)
	}

	// found
	result = append(result, 1)

	// runtime id
	runtimeIDBytes := make([]byte, 4)
	binary.LittleEndian.PutUint32(runtimeIDBytes, runtimeID)
	result = append(result, runtimeIDBytes...)

	return asCbytes(result)
}

//export SubChunkNetworkPayload
func SubChunkNetworkPayload(subChunkId C.longlong, rangeStart C.int, rangeEnd C.int, ind C.int) *C.char {
	return subChunkPayload(subChunkId, rangeStart, rangeEnd, ind, chunk.NetworkEncoding)
}

//export FromSubChunkNetworkPayload
func FromSubChunkNetworkPayload(rangeStart C.int, rangeEnd C.int, payload *C.char) (complexReturn *C.char) {
	return fromSubChunkPayload(rangeStart, rangeEnd, payload, chunk.NetworkEncoding)
}

//export SubChunkDiskPayload
func SubChunkDiskPayload(subChunkId C.longlong, rangeStart C.int, rangeEnd C.int, ind C.int) *C.char {
	return subChunkPayload(subChunkId, rangeStart, rangeEnd, ind, chunk.DiskEncoding)
}

//export FromSubChunkDiskPayload
func FromSubChunkDiskPayload(rangeStart C.int, rangeEnd C.int, payload *C.char) (complexReturn *C.char) {
	return fromSubChunkPayload(rangeStart, rangeEnd, payload, chunk.DiskEncoding)
}
