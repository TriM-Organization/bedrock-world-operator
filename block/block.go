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

const (
	UseNeteaseBlockStates    = true
	UseNetworkBlockRuntimeID = true
)

var (
	//go:embed standard_block_states.nbt
	standardblockStateData []byte
	//go:embed netease_block_states.nbt
	neteaseBlockRuntimeID []byte
)

// blockEntry holds a block with its runtime id.
type blockEntry struct {
	block define.BlockState
	rid   uint32
}

var (
	// blockProperties ..
	blockProperties = map[string]map[string]any{}
	// blockStateMapping holds a map for looking up a block entry by the network runtime id it produces.
	blockStateMapping = map[uint32]blockEntry{}
)

func init() {
	RuntimeIDToState = func(runtimeID uint32) (name string, properties map[string]any, found bool) {
		s, found := blockStateMapping[runtimeID]
		if found {
			return s.block.Name, s.block.Properties, true
		}
		return "", nil, false
	}
	StateToRuntimeID = func(name string, properties map[string]any) (runtimeID uint32, found bool) {
		networkRuntimeID := ComputeBlockHash(name, properties)
		if s, ok := blockStateMapping[networkRuntimeID]; ok {
			return s.rid, true
		}
		networkRuntimeID = ComputeBlockHash(name, blockProperties[name])
		s, ok := blockStateMapping[networkRuntimeID]
		return s.rid, ok
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
// The function panics if UseNetworkBlockRuntimeID is false and the blockState
// was already registered.
func registerBlockState(s define.BlockState) {
	var rid uint32
	hash := ComputeBlockHash(s.Name, s.Properties)

	if !UseNetworkBlockRuntimeID {
		if _, ok := blockStateMapping[hash]; ok {
			panic(fmt.Sprintf("cannot register the same state twice (%+v)", s))
		}
	}

	if _, ok := blockProperties[s.Name]; !ok {
		blockProperties[s.Name] = s.Properties
	}

	if UseNetworkBlockRuntimeID {
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
