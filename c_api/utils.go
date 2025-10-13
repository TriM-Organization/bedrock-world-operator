package main

import "C"
import (
	"bytes"
	"encoding/binary"
	"unsafe"

	"github.com/TriM-Organization/bedrock-world-operator/block"
	"github.com/TriM-Organization/bedrock-world-operator/chunk"
	"github.com/TriM-Organization/bedrock-world-operator/define"
)

func asCbool(b bool) C.int {
	if b {
		return C.int(1)
	}
	return C.int(0)
}

func asGoBool(b C.int) bool {
	return (int(b) != 0)
}

func asCbytes(b []byte) *C.char {
	result := make([]byte, 4)
	binary.LittleEndian.PutUint32(result, uint32(len(b)))
	result = append(result, b...)
	return (*C.char)(C.CBytes(result))
}

func asGoBytes(p *C.char) []byte {
	l := binary.LittleEndian.Uint32(C.GoBytes(unsafe.Pointer(p), 4))
	return C.GoBytes(unsafe.Pointer(p), C.int(4+l))[4:]
}

func packChunkRangeAndID(r define.Range, chunkID int) (complexReturn *C.char) {
	result := make([]byte, 0)

	r1 := make([]byte, 2)
	binary.LittleEndian.PutUint16(r1, uint16(r[0]))
	result = append(result, r1...)

	r2 := make([]byte, 2)
	binary.LittleEndian.PutUint16(r2, uint16(r[1]))
	result = append(result, r2...)

	cID := make([]byte, 8)
	binary.LittleEndian.PutUint64(cID, uint64(chunkID))
	result = append(result, cID...)

	return asCbytes(result)
}

func packDenseBlockMatrix(blockMatrix [][]uint32, subLength int) (encodeBytes []byte) {
	encodeBytes = make([]byte, len(blockMatrix)*subLength*4)

	ptr := 0
	for _, value := range blockMatrix {
		for _, v := range value {
			runtimeIDBytes := make([]byte, 4)
			binary.LittleEndian.PutUint32(runtimeIDBytes, v)
			encodeBytes[ptr], encodeBytes[ptr+1], encodeBytes[ptr+2], encodeBytes[ptr+3] = runtimeIDBytes[0], runtimeIDBytes[1], runtimeIDBytes[2], runtimeIDBytes[3]
			ptr += 4
		}
	}

	return
}

func unpackDenseBlockMatrix(encodeBytes []byte, subLength int) (blockMatrix [][]uint32) {
	blockMatrix = make([][]uint32, len(encodeBytes)/subLength/4)

	ptr := 0
	for i := range len(blockMatrix) {
		blockMatrix[i] = make([]uint32, subLength)
		for j := range subLength {
			blockMatrix[i][j] = binary.LittleEndian.Uint32(encodeBytes[ptr : ptr+4])
			ptr += 4
		}
	}

	return
}

func unpackStateEnums(paylod *C.char) (stateEnums []block.StateEnum) {
	goBytes := asGoBytes(paylod)

	ptr := 1
	stateEnums = make([]block.StateEnum, goBytes[0])

	for index := range stateEnums {
		stateEnum := block.StateEnum{}

		stateKeyNameLen := binary.LittleEndian.Uint16(goBytes[ptr : ptr+2])
		stateEnum.StateKeyName = string(goBytes[ptr+2 : ptr+2+int(stateKeyNameLen)])
		ptr += 2 + int(stateKeyNameLen)

		stateEnum.PossibleValues = make([]any, goBytes[ptr])
		ptr++
		if len(stateEnum.PossibleValues) == 0 {
			continue
		}

		possibleValuesType := goBytes[ptr]
		ptr++

		switch possibleValuesType {
		case 0: // TAG_Byte
			for i := range stateEnum.PossibleValues {
				stateEnum.PossibleValues[i] = goBytes[ptr]
				ptr++
			}
		case 1: // TAG_Int
			for i := range stateEnum.PossibleValues {
				stateEnum.PossibleValues[i] = int32(binary.LittleEndian.Uint32(goBytes[ptr : ptr+4]))
				ptr += 4
			}
		case 2: // TAG_String
			for i := range stateEnum.PossibleValues {
				stringLen := binary.LittleEndian.Uint16(goBytes[ptr : ptr+2])
				stateEnum.PossibleValues[i] = string(goBytes[ptr+2 : ptr+2+int(stringLen)])
				ptr += 2 + int(stringLen)
			}
		}

		stateEnums[index] = stateEnum
	}

	return
}

func fromSubChunkPayload(
	blockTableId C.longlong,
	rangeStart C.int,
	rangeEnd C.int,
	payload *C.char,
	e chunk.Encoding,
) (complexReturn *C.char) {
	t := savedBlockTable.LoadObject(int(blockTableId))
	if t == nil {
		// block table not found
		return asCbytes([]byte{0})
	}

	s, ind, err := chunk.DecodeSubChunk(
		bytes.NewBuffer(asGoBytes(payload)),
		define.Range{int(rangeStart), int(rangeEnd)},
		e,
		*t,
	)
	if err != nil {
		// decode sub chunk failed
		return asCbytes([]byte{0})
	}

	idBytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(idBytes, uint64(savedSubChunk.AddObject(s)))

	// successful
	result := []byte{1, byte(ind)}
	result = append(result, idBytes...)

	return asCbytes(result)
}

func subChunkPayload(
	subChunkId C.longlong,
	blockTableId C.longlong,
	rangeStart C.int,
	rangeEnd C.int,
	ind C.int,
	e chunk.Encoding,
) *C.char {
	r := define.Range{int(rangeStart), int(rangeEnd)}

	s := savedSubChunk.LoadObject(int(subChunkId))
	if s == nil {
		return asCbytes(nil)
	}

	t := savedBlockTable.LoadObject(int(blockTableId))
	if t == nil {
		return asCbytes(nil)
	}

	return asCbytes(chunk.EncodeSubChunk(*s, r, int(ind), e, *t))
}
