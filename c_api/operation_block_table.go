package main

import "C"
import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strings"

	"github.com/Happy2018new/worldupgrader/blockupgrader"
	"github.com/TriM-Organization/bedrock-world-operator/block"
	"github.com/TriM-Organization/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

var savedBlockTable = NewSimpleManager[*block.BlockRuntimeIDTable]()

//export NewBlockTable
func NewBlockTable(useNetworkIDHashes C.int) C.longlong {
	t := block.NewBlockRuntimeIDTable(asGoBool(useNetworkIDHashes))
	return C.longlong(savedBlockTable.AddObject(t))
}

//export ReleaseBlockTable
func ReleaseBlockTable(id C.longlong) {
	savedBlockTable.ReleaseObject(int(id))
}

//export Table_AirRuntimeID
func Table_AirRuntimeID(id C.longlong) C.int {
	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		return -1
	}
	return C.int((*t).AirRuntimeID())
}

//export Table_UseNetworkIDHashes
func Table_UseNetworkIDHashes(id C.longlong) C.int {
	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		return -1
	}
	return asCbool((*t).UseNetworkIDHashes())
}

//export Table_RuntimeIDToState
func Table_RuntimeIDToState(id C.longlong, runtimeID C.int) (complexReturn *C.char) {
	result := make([]byte, 0)

	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		// table not exist
		result = append(result, 0)
		return asCbytes(result)
	}

	name, states, found := (*t).RuntimeIDToState(uint32(runtimeID))
	if !found {
		// runtime ID not found
		result = append(result, 0)
		return asCbytes(result)
	}

	// found
	result = append(result, 1)

	// block name
	nameLength := make([]byte, 2)
	binary.LittleEndian.PutUint16(nameLength, uint16(len(name)))
	result = append(result, nameLength...)
	result = append(result, []byte(name)...)

	// block states NBT
	buf := bytes.NewBuffer(nil)
	nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian).Encode(states)
	nbtLength := make([]byte, 4)
	binary.LittleEndian.PutUint32(nbtLength, uint32(buf.Len()))
	result = append(result, nbtLength...)
	result = append(result, buf.Bytes()...)

	return asCbytes(result)
}

//export Table_StateToRuntimeID
func Table_StateToRuntimeID(id C.longlong, name *C.char, states *C.char) (complexReturn *C.char) {
	var blockStates map[string]any
	result := make([]byte, 0)

	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		// table not exist
		result = append(result, 0)
		return asCbytes(result)
	}

	blockName := C.GoString(name)
	err := nbt.NewDecoderWithEncoding(bytes.NewBuffer(asGoBytes(states)), nbt.LittleEndian).Decode(&blockStates)
	if err != nil {
		// block states NBT decode failed
		result = append(result, 0)
		return asCbytes(result)
	}

	// Make sure the block that come from standard Minecraft can upgrade correctly.
	if !strings.HasPrefix(blockName, "minecraft:") {
		blockName = "minecraft:" + blockName
	}
	upgraded := blockupgrader.Upgrade(blockupgrader.BlockState{
		Name:       blockName,
		Properties: blockStates,
	})

	// First we try the block who have "minecraft:" prefix.
	runtimeID, found := (*t).StateToRuntimeID(upgraded.Name, upgraded.Properties)
	if !found {
		// Otherwise this block maybe is a custom block,
		// and we should trim the prefix and try again.
		upgraded.Name = strings.TrimPrefix(upgraded.Name, "minecraft:")
		runtimeID, found = (*t).StateToRuntimeID(upgraded.Name, upgraded.Properties)
	}
	if !found {
		// corresponding runtime ID not found
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

//export Table_RegisterCustomBlock
func Table_RegisterCustomBlock(id C.longlong, name *C.char, states *C.char, version C.int) *C.char {
	var blockStates map[string]any

	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		return C.CString("Table_RegisterCustomBlock: Block runtime ID table not found")
	}

	err := nbt.NewDecoderWithEncoding(bytes.NewBuffer(asGoBytes(states)), nbt.LittleEndian).Decode(&blockStates)
	if err != nil {
		return C.CString(fmt.Sprintf("Table_RegisterCustomBlock: %v", err))
	}

	err = (*t).RegisterCustomBlock(define.BlockState{
		Name:       C.GoString(name),
		Properties: blockStates,
		Version:    int32(version),
	})
	if err != nil {
		return C.CString(fmt.Sprintf("Table_RegisterCustomBlock: %v", err))
	}

	return C.CString("")
}

//export Table_RegisterPermutation
func Table_RegisterPermutation(id C.longlong, name *C.char, version C.int, stateEnums *C.char) *C.char {
	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		return C.CString("Table_RegisterPermutation: Block runtime ID table not found")
	}

	err := (*t).RegisterPermutation(
		C.GoString(name),
		int32(version),
		unpackStateEnums(stateEnums),
	)
	if err != nil {
		return C.CString(fmt.Sprintf("Table_RegisterPermutation: %v", err))
	}

	return C.CString("")
}

//export Table_FinaliseRegister
func Table_FinaliseRegister(id C.longlong) *C.char {
	t := savedBlockTable.LoadObject(int(id))
	if t == nil {
		return C.CString("Table_FinaliseRegister: Block runtime ID table not found")
	}
	(*t).FinaliseRegister()
	return C.CString("")
}
