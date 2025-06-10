package main

import (
	"runtime/cgo"
)

type SimpleManager[T any] struct{}

func NewSimpleManager[T any]() SimpleManager[T] {
	return SimpleManager[T]{}
}

func (s SimpleManager[T]) AddObject(t T) int {
	return int(cgo.NewHandle(&t))
}

func (s SimpleManager[T]) LoadObject(id int) *T {
	return cgo.Handle(id).Value().(*T)
}

func (s SimpleManager[T]) ReleaseObject(id int) {
	cgo.Handle(id).Delete()
}
