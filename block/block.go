package block

import (
	_ "embed"
	"fmt"
	"sort"
	"strings"

	intintmap "github.com/TriM-Organization/bedrock-world-operator/block/initintmap"
	"github.com/TriM-Organization/bedrock-world-operator/define"
	"github.com/segmentio/fasthash/fnv1"
)

// BlockRuntimeIDTable is a block runtime ID table that
// supports converting blocks between blocks themselves
// and their runtime IDs description.
type BlockRuntimeIDTable struct {
	useNetworkIDHashes    bool
	airBlockRuntimeID     uint32
	blockEntries          []BlockEntry
	blockHashToEntryIndex *intintmap.Map
	defaultBlockStates    map[string]BlockEntry
}

// NewBlockRuntimeIDTable returns a new BlockRuntimeIDTable.
// useNetworkIDHashes indicates whether the runtime IDs are the network ID hashes.
func NewBlockRuntimeIDTable(useNetworkIDHashes bool) *BlockRuntimeIDTable {
	airBlockRuntimeID := uint32(0)
	blockEntries := make([]BlockEntry, len(blockStates))
	blockHashToEntryIndex := intintmap.New(len(blockStates), 0.60)
	defaultBlockStates := make(map[string]BlockEntry)

	for index, value := range blockStates {
		hash := ComputeBlockHash(value.Name, value.Properties)

		_, found := blockHashToEntryIndex.Get(int64(hash))
		if found {
			panic(fmt.Sprintf("NewBlockRuntimeIDTable: Cannot register the same state twice (%+v)", value))
		}

		rid := uint32(index)
		if useNetworkIDHashes {
			rid = hash
		}
		if value.Name == "minecraft:air" {
			airBlockRuntimeID = rid
		}
		entry := BlockEntry{
			Block:     value,
			RuntimeID: rid,
		}

		blockEntries[index] = entry
		blockHashToEntryIndex.Put(int64(hash), int64(index))
		if _, ok := defaultBlockStates[value.Name]; !ok {
			defaultBlockStates[value.Name] = entry
		}
	}

	return &BlockRuntimeIDTable{
		useNetworkIDHashes:    useNetworkIDHashes,
		airBlockRuntimeID:     airBlockRuntimeID,
		blockEntries:          blockEntries,
		blockHashToEntryIndex: blockHashToEntryIndex,
		defaultBlockStates:    defaultBlockStates,
	}
}

// AirRuntimeID returns the runtime ID of the air block.
func (b *BlockRuntimeIDTable) AirRuntimeID() (runtimeID uint32) {
	return b.airBlockRuntimeID
}

// UseNetworkIDHashes returns if the block runtime IDs are using network hashes or not.
func (b *BlockRuntimeIDTable) UseNetworkIDHashes() bool {
	return b.useNetworkIDHashes
}

// RuntimeIDToState converts a runtime ID to a name and its state properties.
func (b *BlockRuntimeIDTable) RuntimeIDToState(runtimeID uint32) (name string, properties map[string]any, found bool) {
	if b.useNetworkIDHashes {
		if index, found := b.blockHashToEntryIndex.Get(int64(runtimeID)); found {
			entry := b.blockEntries[index]
			return entry.Block.Name, entry.Block.Properties, true
		}
		return "", nil, false
	}
	if runtimeID < uint32(len(b.blockEntries)) {
		entry := b.blockEntries[runtimeID]
		return entry.Block.Name, entry.Block.Properties, true
	}
	return "", nil, false
}

// StateToRuntimeID converts a name and its state properties to a runtime ID.
func (b *BlockRuntimeIDTable) StateToRuntimeID(name string, properties map[string]any) (runtimeID uint32, found bool) {
	if index, found := b.blockHashToEntryIndex.Get(int64(ComputeBlockHash(name, properties))); found {
		return b.blockEntries[index].RuntimeID, true
	}
	if entry, ok := b.defaultBlockStates[name]; ok {
		return entry.RuntimeID, true
	}
	if !strings.HasPrefix(name, "minecraft:") {
		return b.StateToRuntimeID("minecraft:"+name, properties)
	}
	return 0, false
}

// RegisterCustomBlock registers a new custom block to the table.
// The function returns error if the block was already registered.
// Note that you MUST call FinaliseRegister atfer register all custom blocks.
func (b *BlockRuntimeIDTable) RegisterCustomBlock(block define.BlockState) error {
	hash := ComputeBlockHash(block.Name, block.Properties)

	_, found := b.blockHashToEntryIndex.Get(int64(hash))
	if found {
		return fmt.Errorf("RegisterCustomBlock: Cannot register the same block twice; block = %#v", block)
	}

	entry := BlockEntry{
		Block:     block,
		RuntimeID: hash,
	}
	b.blockHashToEntryIndex.Put(int64(hash), int64(len(b.blockEntries)))
	b.blockEntries = append(b.blockEntries, entry)

	if b.useNetworkIDHashes {
		_, ok := b.defaultBlockStates[block.Name]
		if !ok {
			b.defaultBlockStates[block.Name] = entry
		}
	}

	return nil
}

// RegisterMultipleStates registers all block
// states of a custom block to the table.
//
// stateEnums is a list of state enums that
// the block can have. Each element means a
// state key and its possible values.
//
// The function returns error if any of the
// states was already registered.
//
// Note that you MUST call FinaliseRegister
// after register all custom blocks.
func (b *BlockRuntimeIDTable) RegisterPermutation(blockName string, blockVersion int32, stateEnums []StateEnum) error {
	permutations := make([]map[string]any, 0)
	stepCounter := make([]int, len(stateEnums))

	for {
		var shouldBreak bool

		permutation := make(map[string]any)
		for index, value := range stepCounter {
			stateEnum := stateEnums[index]
			permutation[stateEnum.StateKeyName] = stateEnum.PossibleValues[value]
		}
		permutations = append(permutations, permutation)

		stepCounter[0]++
		for index, value := range stepCounter {
			if value < len(stateEnums[index].PossibleValues) {
				break
			}

			stepCounter[index] = 0
			if index+1 == len(stepCounter) {
				shouldBreak = true
				break
			}
			stepCounter[index+1]++
		}

		if shouldBreak {
			break
		}
	}

	for _, permutation := range permutations {
		err := b.RegisterCustomBlock(define.BlockState{
			Name:       blockName,
			Properties: permutation,
			Version:    blockVersion,
		})
		if err != nil {
			return fmt.Errorf("RegisterPermutation: %v", err)
		}
	}

	return nil
}

// FinaliseRegister is called after blocks have finished
// registering and the palette can be sorted and hashed.
func (b *BlockRuntimeIDTable) FinaliseRegister() {
	if b.useNetworkIDHashes {
		return
	}
	b.defaultBlockStates = make(map[string]BlockEntry)

	sort.SliceStable(b.blockEntries, func(i, j int) bool {
		nameOne := b.blockEntries[i].Block.Name
		nameTwo := b.blockEntries[j].Block.Name
		return nameOne != nameTwo && fnv1.HashString64(nameOne) < fnv1.HashString64(nameTwo)
	})

	for index, value := range b.blockEntries {
		hash := ComputeBlockHash(value.Block.Name, value.Block.Properties)

		entry := BlockEntry{
			Block:     value.Block,
			RuntimeID: uint32(index),
		}
		if value.Block.Name == "minecraft:air" {
			b.airBlockRuntimeID = entry.RuntimeID
		}

		b.blockEntries[index] = entry
		b.blockHashToEntryIndex.Put(int64(hash), int64(index))
		if _, ok := b.defaultBlockStates[value.Block.Name]; !ok {
			b.defaultBlockStates[value.Block.Name] = entry
		}
	}
}
