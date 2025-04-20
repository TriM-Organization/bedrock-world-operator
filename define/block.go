package define

// BlockState holds a combination of a name and properties, together with a version.
type BlockState struct {
	Name       string         `nbt:"name"`
	Properties map[string]any `nbt:"states"`
	Version    int32          `nbt:"version"`
}

// StateHash is a struct that may be used as a map key for block states. It contains the name of the block state
// and an encoded version of the properties.
type StateHash struct {
	Name       string
	Properties string
}
