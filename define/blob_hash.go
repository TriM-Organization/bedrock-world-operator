package define

import "fmt"

// HashWithPosY ..
type HashWithPosY struct {
	Hash uint64
	PosY int8
}

func (h HashWithPosY) String() string {
	return fmt.Sprintf("%d (y=%d)", h.Hash, h.PosY)
}
