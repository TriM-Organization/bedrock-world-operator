package block

import (
	"bytes"
	"compress/gzip"
	_ "embed"
	"fmt"
	"io"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

const UseNeteaseBlockStates = true

var (
	//go:embed standard_block_states.nbt
	standardblockStateData []byte
	//go:embed netease_block_states.nbt
	neteaseBlockRuntimeID []byte
)

var (
	blockProperties = map[string]map[string]any{}
	// stateRuntimeIDs holds a map for looking up the runtime ID of a block by the network runtime id it produces.
	stateRuntimeIDs = map[uint32]uint32{}
	// stateRuntimeMapping holds a map for looking up a block by the network runtime id it produces.
	stateRuntimeMapping = map[uint32]define.BlockState{}
)

func init() {
	RuntimeIDToState = func(runtimeID uint32) (name string, properties map[string]any, found bool) {
		s, found := stateRuntimeMapping[runtimeID]
		if found {
			return s.Name, s.Properties, true
		}
		return "", nil, false
	}
	StateToRuntimeID = func(name string, properties map[string]any) (runtimeID uint32, found bool) {
		s := define.BlockState{
			Name:       name,
			Properties: properties,
		}

		networkRuntimeID := ComputeBlockHash(s)
		if rid, ok := stateRuntimeIDs[networkRuntimeID]; ok {
			return rid, true
		}

		s.Properties = blockProperties[name]
		networkRuntimeID = ComputeBlockHash(s)
		rid, ok := stateRuntimeIDs[networkRuntimeID]
		return rid, ok
	}

	if UseNeteaseBlockStates {
		var neteaseBlocks []map[string]any
		gzipReader, err := gzip.NewReader(bytes.NewBuffer(neteaseBlockRuntimeID))
		if err != nil {
			panic(`init: Failed to unzip "netease_block_states.nbt" (Stage 1)`)
		}

		unzipedBytes, err := io.ReadAll(gzipReader)
		if err != nil {
			panic(`init: Failed to unzip "netease_block_states.nbt" (Stage 2)`)
		}

		err = nbt.NewDecoderWithEncoding(bytes.NewBuffer(unzipedBytes), nbt.BigEndian).Decode(&neteaseBlocks)
		if err != nil {
			panic("init: Failed to decode netease blocks from NBT")
		}

		// Register all block states present in the block_states.nbt file. These are all possible options registered
		// blocks may encode to.
		for _, value := range neteaseBlocks {
			s := define.BlockState{
				Name:       value["name"].(string),
				Properties: value["states"].(map[string]any),
				Version:    value["version"].(int32),
			}
			registerBlockState(s)
		}

		return
	}

	dec := nbt.NewDecoder(bytes.NewBuffer(standardblockStateData))

	// Register all block states present in the block_states.nbt file. These are all possible options registered
	// blocks may encode to.
	var s define.BlockState
	for {
		if err := dec.Decode(&s); err != nil {
			break
		}
		registerBlockState(s)
	}
}

// registerBlockState registers a new blockState to the states slice.
// The function panics if UseNeteaseBlockStates is false and the blockState
// was already registered.
func registerBlockState(s define.BlockState) {
	var rid uint32
	hash := ComputeBlockHash(s)

	if !UseNeteaseBlockStates {
		if _, ok := stateRuntimeIDs[hash]; ok {
			panic(fmt.Sprintf("cannot register the same state twice (%+v)", s))
		}
	}

	if _, ok := blockProperties[s.Name]; !ok {
		blockProperties[s.Name] = s.Properties
	}

	if UseNeteaseBlockStates {
		rid = hash
	} else {
		rid = uint32(len(stateRuntimeIDs))
	}

	if s.Name == "minecraft:air" {
		AirRuntimeID = rid
	}

	stateRuntimeIDs[hash] = rid
	stateRuntimeMapping[hash] = s
}
