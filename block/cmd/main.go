package main

import (
	"bytes"
	"cmp"
	"compress/gzip"
	_ "embed"
	"fmt"
	"io"
	"os"
	"slices"

	block_general "github.com/TriM-Organization/bedrock-world-operator/block/general"
	"github.com/TriM-Organization/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
	"github.com/sandertv/gophertunnel/minecraft/protocol"
)

var (
	//go:embed standard_block_states.nbt
	standardBlockStates []byte
	//go:embed netease_block_states.nbt
	neteaseBlockStates []byte
)

var (
	stringSet       []string                 = make([]string, 0)
	blockStatesSet  []block_general.StateKey = make([]block_general.StateKey, 0)
	blockVersionSet []int32                  = make([]int32, 0)
)

var (
	stringToSetIndex       map[string]uint32 = make(map[string]uint32)
	blockStatesToSetIndex  map[string]uint32 = make(map[string]uint32)
	blockVersionToSetIndex map[int32]uint32  = make(map[int32]uint32)
)

func main() {
	fmt.Println("Down, and file saved in ../block_states.bin\n:)")
}

func init() {
	blocks := make([]define.BlockState, 0)

	defer func() {
		initSet(blocks)
		set := genSetBinary()
		blks := genBlockStatesBinary(blocks)
		if err := os.WriteFile("../block_states.bin", append(set, blks...), 0600); err != nil {
			panic(err)
		}
	}()

	if block_general.UseNeteaseBlockStates {
		type nemc struct {
			Blocks []define.NetEaseBlock `nbt:"blocks"`
		}

		var neteaseBlocks nemc
		gzipReader, err := gzip.NewReader(bytes.NewBuffer(neteaseBlockStates))
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
		for _, value := range neteaseBlocks.Blocks {
			blocks = append(blocks, define.BlockState{
				Name:       value.Name,
				Properties: value.States,
				Version:    value.Version,
			})
		}

		return
	}

	dec := nbt.NewDecoder(bytes.NewBuffer(standardBlockStates))

	// Register all block states present in the block_states.nbt file. These are all possible options registered
	// blocks may encode to.
	var s define.BlockState
	for {
		if err := dec.Decode(&s); err != nil {
			break
		}
		blocks = append(blocks, s)
	}
}

func initSet(states []define.BlockState) {
	stringMapping := make(map[string]bool)
	statesMapping := make(map[block_general.StateKey]bool)
	versionMapping := make(map[int32]bool)

	for _, value := range states {
		stringMapping[value.Name] = true
		versionMapping[value.Version] = true
		for key, val := range value.Properties {
			stringMapping[key] = true
			if v, ok := val.(string); ok {
				stringMapping[v] = true
			}
		}
	}

	for key := range stringMapping {
		stringSet = append(stringSet, key)
	}
	for key := range versionMapping {
		blockVersionSet = append(blockVersionSet, key)
	}

	slices.Sort(stringSet)
	slices.Sort(blockVersionSet)

	for index, value := range stringSet {
		stringToSetIndex[value] = uint32(index)
	}
	for index, value := range blockVersionSet {
		blockVersionToSetIndex[value] = uint32(index)
	}

	for _, value := range states {
		for key, val := range value.Properties {
			stateKey := block_general.StateKey{KeyNameIndex: stringToSetIndex[key]}

			switch val.(type) {
			case string:
				stateKey.KeyType = block_general.StateKeyTypeString
			case int32:
				stateKey.KeyType = block_general.StateKeyTypeInt32
			case byte:
				stateKey.KeyType = block_general.StateKeyTypeByte
			default:
				panic(fmt.Sprintf("initSet: Unknown state key type of %#v(%T); key = %#v, block = %#v", val, val, key, value))
			}

			statesMapping[stateKey] = true
		}
	}

	for key := range statesMapping {
		blockStatesSet = append(blockStatesSet, key)
	}

	slices.SortStableFunc(blockStatesSet, func(a block_general.StateKey, b block_general.StateKey) int {
		return cmp.Compare(a.KeyNameIndex, b.KeyNameIndex)
	})

	for index, value := range blockStatesSet {
		keyName := stringSet[value.KeyNameIndex]
		if val, ok := blockStatesToSetIndex[keyName]; ok {
			panic(
				fmt.Sprintf("initSet: Try to overwrite a state who name %#v to a different type; origin = %#v, newer = %#v",
					keyName, blockStatesSet[val].KeyType, value.KeyType,
				),
			)
		}
		blockStatesToSetIndex[keyName] = uint32(index)
	}
}

func sortProperties(in map[string]any) []block_general.IndexBlockProperty {
	result := make([]block_general.IndexBlockProperty, 0)

	keys := make([]string, 0)
	for key := range in {
		keys = append(keys, key)
	}
	slices.Sort(keys)

	for _, key := range keys {
		buf := bytes.NewBuffer(nil)
		w := protocol.NewWriter(buf, 0)

		switch v := in[key].(type) {
		case string:
			ind := uint32(stringToSetIndex[v])
			w.Varuint32(&ind)
			result = append(result, block_general.IndexBlockProperty{
				KeyIndex: blockStatesToSetIndex[key],
				Value:    buf.Bytes(),
			})
		case int32:
			w.Varint32(&v)
			result = append(result, block_general.IndexBlockProperty{
				KeyIndex: blockStatesToSetIndex[key],
				Value:    buf.Bytes(),
			})
		case byte:
			result = append(result, block_general.IndexBlockProperty{
				KeyIndex: blockStatesToSetIndex[key],
				Value:    []byte{v},
			})
		}
	}

	return result
}

func genSetBinary() []byte {
	buf := bytes.NewBuffer(nil)
	w := protocol.NewWriter(buf, 0)

	protocol.FuncSliceUint16Length(w, &stringSet, w.String)
	protocol.FuncSliceUint16Length(w, &blockVersionSet, w.Varint32)
	protocol.SliceUint16Length(w, &blockStatesSet)

	return buf.Bytes()
}

func genBlockStatesBinary(states []define.BlockState) []byte {
	buf := bytes.NewBuffer(nil)
	w := protocol.NewWriter(buf, 0)

	for _, value := range states {
		indexBlockState := block_general.IndexBlockState{
			BlockNameIndex:  stringToSetIndex[value.Name],
			BlockProperties: sortProperties(value.Properties),
			VersionIndex:    blockVersionToSetIndex[value.Version],
		}
		indexBlockState.Marshal(w)
	}

	return buf.Bytes()
}
