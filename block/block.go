package block

import (
	"bytes"
	_ "embed"
	"fmt"
	"sort"
	"strings"
	"unsafe"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

var (
	//go:embed block_states.nbt
	blockStateData []byte

	blockProperties = map[string]map[string]any{}
	// blocks holds a list of all registered Blocks indexed by their runtime ID. Blocks that were not explicitly
	// registered are of the type unknownBlock.
	blocks []define.BlockState
	// stateRuntimeIDs holds a map for looking up the runtime ID of a block by the define.StateHash it produces.
	stateRuntimeIDs = map[define.StateHash]uint32{}
)

func init() {
	dec := nbt.NewDecoder(bytes.NewBuffer(blockStateData))

	// Register all block states present in the block_states.nbt file. These are all possible options registered
	// blocks may encode to.
	var s define.BlockState
	for {
		if err := dec.Decode(&s); err != nil {
			break
		}
		registerBlockState(s)
	}

	RuntimeIDToState = func(runtimeID uint32) (name string, properties map[string]any, found bool) {
		if runtimeID >= uint32(len(blocks)) {
			return "", nil, false
		}
		return blocks[runtimeID].Name, blocks[runtimeID].Properties, true
	}
	StateToRuntimeID = func(name string, properties map[string]any) (runtimeID uint32, found bool) {
		if rid, ok := stateRuntimeIDs[define.StateHash{Name: name, Properties: hashProperties(properties)}]; ok {
			return rid, true
		}
		rid, ok := stateRuntimeIDs[define.StateHash{Name: name, Properties: hashProperties(blockProperties[name])}]
		return rid, ok
	}
}

// registerBlockState registers a new blockState to the states slice. The function panics if the properties the
// blockState hold are invalid or if the blockState was already registered.
func registerBlockState(s define.BlockState) {
	h := define.StateHash{Name: s.Name, Properties: hashProperties(s.Properties)}
	if _, ok := stateRuntimeIDs[h]; ok {
		panic(fmt.Sprintf("cannot register the same state twice (%+v)", s))
	}
	if _, ok := blockProperties[s.Name]; !ok {
		blockProperties[s.Name] = s.Properties
	}
	rid := uint32(len(blocks))
	blocks = append(blocks, s)

	if s.Name == "minecraft:air" {
		AirRuntimeID = rid
	}

	stateRuntimeIDs[h] = rid
}

// hashProperties produces a hash for the block properties held by the blockState.
func hashProperties(properties map[string]any) string {
	if properties == nil {
		return ""
	}
	keys := make([]string, 0, len(properties))
	for k := range properties {
		keys = append(keys, k)
	}
	sort.Slice(keys, func(i, j int) bool {
		return keys[i] < keys[j]
	})

	var b strings.Builder
	for _, k := range keys {
		switch v := properties[k].(type) {
		case bool:
			if v {
				b.WriteByte(1)
			} else {
				b.WriteByte(0)
			}
		case uint8:
			b.WriteByte(v)
		case int32:
			a := *(*[4]byte)(unsafe.Pointer(&v))
			b.Write(a[:])
		case string:
			b.WriteString(v)
		default:
			// If block encoding is broken, we want to find out as soon as possible. This saves a lot of time
			// debugging in-game.
			panic(fmt.Sprintf("invalid block property type %T for property %v", v, k))
		}
	}

	return b.String()
}
