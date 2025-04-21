package main

import (
	"maps"
	"sync"
)

type SimpleManager[T any] struct {
	mapping map[int]*T
	mu      *sync.RWMutex
	ptr     int
}

func NewSimpleManager[T any]() *SimpleManager[T] {
	return &SimpleManager[T]{
		mapping: make(map[int]*T),
		mu:      new(sync.RWMutex),
		ptr:     -1,
	}
}

func (s *SimpleManager[T]) AddObject(t T) int {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.ptr++
	s.mapping[s.ptr] = &t
	return s.ptr
}

func (s *SimpleManager[T]) LoadObject(id int) *T {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.mapping[id]
}

func (s *SimpleManager[T]) ReleaseObject(id int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.mapping, id)
	newMapping := make(map[int]*T)
	maps.Copy(newMapping, s.mapping)
	s.mapping = newMapping
}
