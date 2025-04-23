package block

import (
	"bytes"
	_ "embed"
	"fmt"
	"strings"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

const UseNeteaseBlockStates = true

// blockEntry holds a block with its runtime id.
type blockEntry struct {
	block define.BlockState
	rid   uint32
}

var (
	//go:embed block_states.nbt
	blockStateData []byte

	// blockProperties ..
	blockProperties = map[string]map[string]any{}
	// blockStateMapping holds a map for looking up a block entry by the network runtime id it produces.
	blockStateMapping = map[uint32]blockEntry{}
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
		s, found := blockStateMapping[runtimeID]
		if found {
			return s.block.Name, s.block.Properties, true
		}
		return "", nil, false
	}
	StateToRuntimeID = func(name string, properties map[string]any) (runtimeID uint32, found bool) {
		if !strings.Contains(name, "minecraft:") {
			name = "minecraft:" + name
		}

		networkRuntimeID := ComputeBlockHash(name, properties)
		if s, ok := blockStateMapping[networkRuntimeID]; ok {
			return s.rid, true
		}

		networkRuntimeID = ComputeBlockHash(name, blockProperties[name])
		s, ok := blockStateMapping[networkRuntimeID]
		return s.rid, ok
	}
}

// registerBlockState registers a new blockState to the states slice.
// The function panics if UseNeteaseBlockStates is false and the blockState
// was already registered.
// Additionally, if UseNeteaseBlockStates is true, then the runtime id
// will register as the network block hash.
func registerBlockState(s define.BlockState) {
	var rid uint32
	hash := ComputeBlockHash(s.Name, s.Properties)

	if !UseNeteaseBlockStates {
		if _, ok := blockStateMapping[hash]; ok {
			panic(fmt.Sprintf("cannot register the same state twice (%+v)", s))
		}
	}

	if _, ok := blockProperties[s.Name]; !ok {
		blockProperties[s.Name] = s.Properties
	}

	if UseNeteaseBlockStates {
		rid = hash
	} else {
		rid = uint32(len(blockStateMapping))
	}

	if s.Name == "minecraft:air" {
		AirRuntimeID = rid
	}

	blockStateMapping[hash] = blockEntry{
		block: s,
		rid:   rid,
	}
}
