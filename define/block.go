package define

// BlockState holds a combination of a name and properties, together with a version.
type BlockState struct {
	Name       string         `nbt:"name"`
	Properties map[string]any `nbt:"states"`
	Version    int32          `nbt:"version"`
}

// NetEaseBlock is the represents of a block in NetEase
type NetEaseBlock struct {
	Name           string         `nbt:"name"`
	NameHash       int64          `nbt:"name_hash"`
	BlockRuntimeID int32          `nbt:"network_id"`
	States         map[string]any `nbt:"states"`
	Val            int16          `nbt:"val"`
	Version        int32          `nbt:"version"`
}
