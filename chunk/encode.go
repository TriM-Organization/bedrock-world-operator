package chunk

import (
	"bytes"
	"sync"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
)

const (
	// SubChunkVersion is the current version of the written sub chunks, specifying the format they are
	// written on disk and over network.
	SubChunkVersion = 9
	// CurrentBlockVersion is the current version of blocks (states) of the game. This version is composed
	// of 4 bytes indicating a version, interpreted as a big endian int. The current version represents
	// 1.16.0.14 {1, 16, 0, 14}.
	CurrentBlockVersion int32 = 18100737
)

// pool is used to pool byte buffers used for encoding chunks.
var pool = sync.Pool{
	New: func() any {
		return bytes.NewBuffer(make([]byte, 0, 1024))
	},
}

// SerialisedData holds the serialised data of a  It consists of the chunk's block data itself, a height
// map, the biomes and entities and block entities.
type SerialisedData struct {
	// sub holds the data of the serialised sub chunks in a  Sub chunks that are empty or that otherwise
	// don't exist are represented as an empty slice (or technically, nil).
	SubChunks [][]byte
	// Biomes is the biome data of the chunk, which is composed of a biome storage for each sub-
	Biomes []byte
}

// Encode encodes Chunk to an intermediate representation SerialisedData. An Encoding may be passed to encode either for
// network or disk purposed, the most notable difference being that the network encoding generally uses varints and no
// NBT.
func Encode(c *Chunk, e Encoding) SerialisedData {
	d := SerialisedData{SubChunks: make([][]byte, len(c.Sub()))}
	for i, subChunk := range c.Sub() {
		d.SubChunks[i] = EncodeSubChunk(subChunk, c.r, i, e)
	}
	d.Biomes = EncodeBiomes(c, e)
	return d
}

// EncodeSubChunk encodes a sub-chunk from a chunk into bytes. An Encoding may be passed to encode either for network or
// disk purposed, the most notable difference being that the network encoding generally uses varints and no NBT.
func EncodeSubChunk(c *SubChunk, r define.Range, ind int, e Encoding) []byte {
	buf := pool.Get().(*bytes.Buffer)
	defer func() {
		buf.Reset()
		pool.Put(buf)
	}()

	_, _ = buf.Write([]byte{SubChunkVersion, byte(len(c.storages)), uint8(ind + (r[0] >> 4))})
	for _, storage := range c.storages {
		encodePalettedStorage(buf, storage, nil, e, BlockPaletteEncoding)
	}

	sub := make([]byte, buf.Len())
	_, _ = buf.Read(sub)

	return sub
}

// EncodeBiomes encodes the biomes of a chunk into bytes. An Encoding may be passed to encode either for network or
// disk purposed, the most notable difference being that the network encoding generally uses varints and no NBT.
func EncodeBiomes(c *Chunk, e Encoding) []byte {
	buf := pool.Get().(*bytes.Buffer)
	defer func() {
		buf.Reset()
		pool.Put(buf)
	}()

	var previous *PalettedStorage
	for _, b := range c.biomes {
		encodePalettedStorage(buf, b, previous, e, BiomePaletteEncoding)
		previous = b
	}
	biomes := make([]byte, buf.Len())
	_, _ = buf.Read(biomes)
	return biomes
}

// encodePalettedStorage encodes a PalettedStorage into a bytes.Buffer. The Encoding passed is used to write the Palette
// of the PalettedStorage.
func encodePalettedStorage(buf *bytes.Buffer, storage, previous *PalettedStorage, e Encoding, pe paletteEncoding) {
	if storage.Equal(previous) {
		_, _ = buf.Write([]byte{0x7f<<1 | e.network()})
		return
	}
	b := make([]byte, len(storage.indices)*4+1)
	b[0] = byte(storage.bitsPerIndex<<1) | e.network()

	for i, v := range storage.indices {
		// Explicitly don't use the binary package to greatly improve performance of writing the uint32s.
		b[i*4+1], b[i*4+2], b[i*4+3], b[i*4+4] = byte(v), byte(v>>8), byte(v>>16), byte(v>>24)
	}
	_, _ = buf.Write(b)

	e.encodePalette(buf, storage.Palette(), pe)
}
