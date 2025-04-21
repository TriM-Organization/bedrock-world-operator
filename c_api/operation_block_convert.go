package main

import "C"
import (
	"bytes"
	"encoding/binary"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/block"
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

	runtimeID, found := block.StateToRuntimeID(blockName, blockStates)
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
