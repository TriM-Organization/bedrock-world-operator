package main

import (
	"runtime"
	"sync"
	"unsafe"
)

type SimpleManager[T any] struct {
	mapping sync.Map // map[uintptr]*runtime.Pinner
}

func NewSimpleManager[T any]() *SimpleManager[T] {
	return &SimpleManager[T]{
		mapping: sync.Map{},
	}
}

func (s *SimpleManager[T]) AddObject(t T) int {
	goPtr := &t

	pinner := new(runtime.Pinner)
	pinner.Pin(goPtr)

	ptr := uintptr(unsafe.Pointer(goPtr))
	s.mapping.Store(ptr, pinner)

	return int(ptr)
}

func (s *SimpleManager[T]) LoadObject(ptr int) *T {
	return (*T)(unsafe.Pointer(uintptr(ptr)))
}

func (s *SimpleManager[T]) ReleaseObject(ptr int) {
	value, ok := s.mapping.LoadAndDelete(uintptr(ptr))
	if !ok {
		return
	}

	pinner, ok := value.(*runtime.Pinner)
	if !ok {
		return
	}

	pinner.Unpin()
}
