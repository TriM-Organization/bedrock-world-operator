package block_general

import "github.com/sandertv/gophertunnel/minecraft/protocol"

const (
	StateKeyTypeString uint8 = iota
	StateKeyTypeInt32
	StateKeyTypeByte
)

type SingleStateKey struct {
	KeyName string
	KeyType uint8
}

func (s *SingleStateKey) Marshal(io protocol.IO) {
	io.String(&s.KeyName)
	io.Uint8(&s.KeyType)
}

type IndexBlockProperty struct {
	Index uint32
	Value []byte
}

func (i *IndexBlockProperty) Marshal(io protocol.IO) {
	io.Varuint32(&i.Index)
	io.ByteSlice(&i.Value)
}

type IndexBlockState struct {
	BlockNameIndex  uint32
	BlockProperties []IndexBlockProperty
	VersionIndex    uint32
}

func (i *IndexBlockState) Marshal(io protocol.IO) {
	io.Varuint32(&i.BlockNameIndex)
	io.Varuint32(&i.VersionIndex)
	protocol.SliceUint16Length(io, &i.BlockProperties)
}
