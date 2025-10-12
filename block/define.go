package block

import (
	"bytes"
	"compress/gzip"
	_ "embed"
	"io"

	"github.com/TriM-Organization/bedrock-world-operator/define"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

var (
	//go:embed block_states.nbt
	blockStatesBytes []byte
	blockStates      []define.BlockState
)

// BlockEntry holds a block with its runtime id.
type BlockEntry struct {
	Block     define.BlockState
	RuntimeID uint32
}

// StateEnum holds a single block property key and its possible values.
type StateEnum struct {
	StateKeyName   string
	PossibleValues []any
}

func init() {
	type nemc struct {
		Blocks []define.NetEaseBlock `nbt:"blocks"`
	}

	var neteaseBlocks nemc
	gzipReader, err := gzip.NewReader(bytes.NewBuffer(blockStatesBytes))
	if err != nil {
		panic(`init: Failed to unzip "netease_block_states.nbt" (Stage 1)`)
	}
	defer gzipReader.Close()

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
		blockStates = append(blockStates, define.BlockState{
			Name:       value.Name,
			Properties: value.States,
			Version:    value.Version,
		})
	}
}
