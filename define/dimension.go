package define

import "fmt"

const (
	DimensionIDOverworld = iota
	DimensionIDNether
	DimensionIDEnd
)

// Dimension is a dimension of a World. It influences a variety of
// properties of a World such as the building range, the sky colour and the
// behaviour of liquid blocks.
type Dimension int32

// Range returns the lowest and highest valid Y coordinates of a block
// in the Dimension.
func (d Dimension) Range() Range {
	switch int32(d) {
	case DimensionIDOverworld:
		return Range{-64, 319}
	case DimensionIDNether:
		return Range{0, 127}
	case DimensionIDEnd:
		return Range{0, 255}
	default:
		return Range{-64, 319}
	}
}

// Height returns the height of this dimension.
// For example, the height of overworld is 384
// due to "384 = 319 - (-64) + 1", and 319 is
// the max Y that overworld could build, and -64
// is the min Y that overworld could build.
func (d Dimension) Height() int {
	r := d.Range()
	return r[1] - r[0] + 1
}

// String ..
func (d Dimension) String() string {
	switch int32(d) {
	case DimensionIDOverworld:
		return "Overworld"
	case DimensionIDNether:
		return "Nether"
	case DimensionIDEnd:
		return "End"
	default:
		return fmt.Sprintf("Custom (id=%d)", int(d))
	}
}
