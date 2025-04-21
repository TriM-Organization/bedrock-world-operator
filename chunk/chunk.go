package chunk

import (
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
)

// Chunk is a segment in the world with a size of 16x16x256 blocks. A chunk contains multiple sub chunks
// and stores other information such as biomes.
// It is not safe to call methods on Chunk simultaneously from multiple goroutines.
type Chunk struct {
	// r holds the (vertical) range of the Chunk. It includes both the minimum and maximum coordinates.
	r define.Range
	// air is the runtime ID of air.
	air uint32
	// sub holds all sub chunks part of the chunk. The pointers held by the array are nil if no sub chunk is
	// allocated at the indices.
	sub []*SubChunk
	// biomes is an array of biome IDs. There is one biome ID for every column in the chunk.
	biomes []*PalettedStorage
}

// NewChunk initialises a new chunk and returns it, so that it may be used.
func NewChunk(air uint32, r define.Range) *Chunk {
	n := (r.Height() >> 4) + 1
	sub, biomes := make([]*SubChunk, n), make([]*PalettedStorage, n)
	for i := range n {
		sub[i] = NewSubChunk(air)
		biomes[i] = emptyStorage(0)
	}
	return &Chunk{
		r:      r,
		air:    air,
		sub:    sub,
		biomes: biomes,
	}
}

// Equals returns if the chunk passed is equal to the current one
func (chunk *Chunk) Equals(c *Chunk) bool {
	if c.r != chunk.r || c.air != chunk.air || len(c.sub) != len(chunk.sub) {
		return false
	}

	for i, s := range c.sub {
		if !s.Equals(chunk.sub[i]) {
			return false
		}
	}

	return true
}

// Range returns the define.Range of the Chunk as passed to NewChunk.
func (chunk *Chunk) Range() define.Range {
	return chunk.r
}

// Sub returns a list of all sub chunks present in the chunk.
func (chunk *Chunk) Sub() []*SubChunk {
	return chunk.sub
}

// Block returns the runtime ID of the block at a given x, y and z in a chunk at the given layer. If no
// sub chunk exists at the given y, the block is assumed to be air.
func (chunk *Chunk) Block(x uint8, y int16, z uint8, layer uint8) uint32 {
	sub := chunk.SubChunk(y)
	if sub.Empty() || uint8(len(sub.storages)) <= layer {
		return chunk.air
	}
	return sub.storages[layer].At(x, uint8(y), z)
}

// SetBlock sets the runtime ID of a block at a given x, y and z in a chunk at the given layer. If no
// SubChunk exists at the given y, a new SubChunk is created and the block is set.
func (chunk *Chunk) SetBlock(x uint8, y int16, z uint8, layer uint8, block uint32) {
	sub := chunk.sub[chunk.SubIndex(y)]
	if uint8(len(sub.storages)) <= layer && block == chunk.air {
		// Air was set at n layer, but there were less than n layers, so there already was air there.
		// Don't do anything with this, just return.
		return
	}
	sub.Layer(layer).Set(x, uint8(y), z, block)
}

// Biome returns the biome ID at a specific column in the chunk.
func (chunk *Chunk) Biome(x uint8, y int16, z uint8) uint32 {
	return chunk.biomes[chunk.SubIndex(y)].At(x, uint8(y), z)
}

// SetBiome sets the biome ID at a specific column in the chunk.
func (chunk *Chunk) SetBiome(x uint8, y int16, z uint8, biome uint32) {
	chunk.biomes[chunk.SubIndex(y)].Set(x, uint8(y), z, biome)
}

// Compact compacts the chunk as much as possible, getting rid of any sub chunks that are empty, and compacts
// all storages in the sub chunks to occupy as little space as possible.
// Compact should be called right before the chunk is saved in order to optimise the storage space.
func (chunk *Chunk) Compact() {
	for i := range chunk.sub {
		chunk.sub[i].compact()
	}
}

// SubChunk finds the correct SubChunk in the Chunk by a Y value.
func (chunk *Chunk) SubChunk(y int16) *SubChunk {
	return chunk.sub[chunk.SubIndex(y)]
}

// SubIndex returns the sub chunk Y index matching the y value passed.
func (chunk *Chunk) SubIndex(y int16) int16 {
	return (y - int16(chunk.r[0])) >> 4
}

// SubY returns the sub chunk Y value matching the index passed.
func (chunk *Chunk) SubY(index int16) int16 {
	return (index << 4) + int16(chunk.r[0])
}

// HighestFilledSubChunk returns the index of the highest sub chunk in the chunk
// that has any blocks in it. 0 is returned if no subchunks have any blocks.
func (chunk *Chunk) HighestFilledSubChunk() uint16 {
	highest := uint16(0)
	for highest = uint16(len(chunk.sub) - 1); highest > 0; highest-- {
		if !chunk.sub[highest].Empty() {
			break
		}
	}
	return highest
}
