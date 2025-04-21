package main

import "C"
import (
	"encoding/binary"
	"unsafe"
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
