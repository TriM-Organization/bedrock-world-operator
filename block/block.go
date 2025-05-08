package block

import (
	"bytes"
	_ "embed"
	"fmt"
	"strings"

	block_general "github.com/YingLunTown-DreamLand/bedrock-world-operator/block/general"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/protocol"
)

// blockEntry holds a block with its runtime id.
type blockEntry struct {
	block block_general.IndexBlockState
	rid   uint32
}

var (
	stringSet       []string                 = make([]string, 0)
	blockStatesSet  []block_general.StateKey = make([]block_general.StateKey, 0)
	blockVersionSet []int32                  = make([]int32, 0)
)

var (
	//go:embed block_states.bin
	blockStates []byte

	// blockProperties ..
	blockProperties = map[string][]block_general.IndexBlockProperty{}
	// blockStateMapping holds a map for looking up a block entry by the network runtime id it produces.
	blockStateMapping = map[uint32]blockEntry{}
)

func init() {
	buf := bytes.NewBuffer(blockStates)
	r := protocol.NewReader(buf, 0, false)

	decodeSet(r)
	for buf.Len() > 0 {
		indexBlockState := block_general.IndexBlockState{}
		indexBlockState.Marshal(r)
		registerBlockState(indexBlockState)
	}

	blockStates = nil

	RuntimeIDToState = func(runtimeID uint32) (name string, properties map[string]any, found bool) {
		s, found := blockStateMapping[runtimeID]
		if found {
			realBlock := decodeToNormalBlockState(s.block)
			return realBlock.Name, realBlock.Properties, true
		}
		return "", nil, false
	}
	StateToRuntimeID = func(name string, properties map[string]any) (runtimeID uint32, found bool) {
		if !strings.HasPrefix(name, "minecraft:") {
			name = "minecraft:" + name
		}

		networkRuntimeID := ComputeBlockHash(name, properties)
		if s, ok := blockStateMapping[networkRuntimeID]; ok {
			return s.rid, true
		}

		networkRuntimeID = ComputeBlockHash(name, decodeToNormalBlockProperties(blockProperties[name]))
		s, ok := blockStateMapping[networkRuntimeID]
		return s.rid, ok
	}
}

func decodeSet(io protocol.IO) {
	protocol.FuncSliceUint16Length(io, &stringSet, io.String)
	protocol.FuncSliceUint16Length(io, &blockVersionSet, io.Varint32)
	protocol.SliceUint16Length(io, &blockStatesSet)
}

func decodeToNormalBlockProperties(p []block_general.IndexBlockProperty) map[string]any {
	result := make(map[string]any)

	for _, value := range p {
		buf := bytes.NewBuffer(value.Value)
		r := protocol.NewReader(buf, 0, false)

		key := blockStatesSet[value.KeyIndex]
		keyName := stringSet[key.KeyNameIndex]

		switch key.KeyType {
		case block_general.StateKeyTypeString:
			var ind uint32
			r.Varuint32(&ind)
			result[keyName] = stringSet[ind]
		case block_general.StateKeyTypeInt32:
			var val int32
			r.Varint32(&val)
			result[keyName] = val
		case block_general.StateKeyTypeByte:
			result[keyName] = value.Value[0]
		}
	}

	return result
}

func decodeToNormalBlockState(s block_general.IndexBlockState) define.BlockState {
	return define.BlockState{
		Name:       stringSet[s.BlockNameIndex],
		Properties: decodeToNormalBlockProperties(s.BlockProperties),
		Version:    blockVersionSet[s.VersionIndex],
	}
}

// registerBlockState registers a new blockState to the states slice.
// The function panics if the blockState was already registered.
func registerBlockState(s block_general.IndexBlockState) {
	var rid uint32

	realBlock := decodeToNormalBlockState(s)
	hash := ComputeBlockHash(realBlock.Name, realBlock.Properties)

	if _, ok := blockStateMapping[hash]; ok {
		panic(fmt.Sprintf("cannot register the same state twice (%+v)", s))
	}

	if _, ok := blockProperties[realBlock.Name]; !ok {
		blockProperties[realBlock.Name] = s.BlockProperties
	}

	if block_general.UseNetworkBlockRuntimeID {
		rid = hash
	} else {
		rid = uint32(len(blockStateMapping))
	}

	if realBlock.Name == "minecraft:air" {
		AirRuntimeID = rid
	}

	blockStateMapping[hash] = blockEntry{
		block: s,
		rid:   rid,
	}
}
