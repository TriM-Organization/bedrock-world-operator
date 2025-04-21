package main

/*
#include <stdio.h>
#include <stdlib.h>
*/
import "C"
import (
	"unsafe"
)

//export FreeMemory
func FreeMemory(address unsafe.Pointer) {
	C.free(address)
}
