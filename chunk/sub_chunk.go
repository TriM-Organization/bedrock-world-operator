package chunk

// SubChunk is a cube of blocks located in a chunk. It has a size of 16x16x16 blocks and forms part of a stack
// that forms a Chunk.
type SubChunk struct {
	air      uint32
	storages []*PalettedStorage
}

// NewSubChunk creates a new sub chunk. All sub chunks should be created through this function
func NewSubChunk(air uint32) *SubChunk {
	return &SubChunk{air: air}
}

// Equals returns if the sub chunk passed is equal to the current one.
func (sub *SubChunk) Equals(s *SubChunk) bool {
	if s.air != sub.air || len(s.storages) != len(sub.storages) {
		return false
	}

	for i, st := range s.storages {
		if !st.Equal(sub.storages[i]) {
			return false
		}
	}

	return true
}

// Empty checks if the SubChunk is considered empty. This is the case if the SubChunk has 0 block storages or if it has
// a single one that is completely filled with air.
func (sub *SubChunk) Empty() bool {
	return len(sub.storages) == 0 || (len(sub.storages) == 1 && len(sub.storages[0].palette.values) == 1 && sub.storages[0].palette.values[0] == sub.air)
}

// Layer returns a certain block storage/layer from a sub chunk. If no storage at the layer exists, the layer
// is created, as well as all layers between the current highest layer and the new highest layer.
func (sub *SubChunk) Layer(layer uint8) *PalettedStorage {
	for uint8(len(sub.storages)) <= layer {
		// Keep appending to storages until the requested layer is achieved. Makes working with new layers
		// much easier.
		sub.storages = append(sub.storages, emptyStorage(sub.air))
	}
	return sub.storages[layer]
}

// Layers returns all layers in the sub chunk. This method may also return an empty slice.
func (sub *SubChunk) Layers() []*PalettedStorage {
	return sub.storages
}

// Block returns the runtime ID of the block located at the given X, Y and Z. X, Y and Z must be in a
// range of 0-15.
func (sub *SubChunk) Block(x, y, z byte, layer uint8) uint32 {
	if uint8(len(sub.storages)) <= layer {
		return sub.air
	}
	return sub.storages[layer].At(x, y, z)
}

// Blocks returns all blocks (block runtime ids) whose in layer.
// If layer is not exist, then return blocks with all air.
// Note that the length of returned slice is 4096 (16*16*16).
func (sub *SubChunk) Blocks(layer uint8) []uint32 {
	result := make([]uint32, 16*16*16)

	if uint8(len(sub.storages)) <= layer {
		for i := range result {
			result[i] = sub.air
		}
		return result
	}

	currentLayer := sub.Layer(layer)

	i := 0
	for x := range byte(16) {
		for y := range byte(16) {
			for z := range byte(16) {
				result[i] = currentLayer.At(x, y, z)
				i++
			}
		}
	}

	return result
}

// SetBlock sets the given block runtime ID at the given X, Y and Z. X, Y and Z must be in a range of 0-15.
func (sub *SubChunk) SetBlock(x, y, z byte, layer uint8, block uint32) {
	sub.Layer(layer).Set(x, y, z, block)
}

// SetBlock sets the whole sub chunk in layer by given block runtime ids.
// len(blocks) must equal to 4096 (16*16*16).
func (sub *SubChunk) SetBlocks(layer uint8, blocks []uint32) {
	currentLayer := sub.Layer(layer)

	i := 0
	for x := range byte(16) {
		for y := range byte(16) {
			for z := range byte(16) {
				currentLayer.Set(x, y, z, blocks[i])
				i++
			}
		}
	}
}

// Compact cleans the garbage from all block storages that sub chunk contains, so that they may be
// cleanly written to a database.
func (sub *SubChunk) compact() {
	newStorages := make([]*PalettedStorage, 0, len(sub.storages))
	for _, storage := range sub.storages {
		storage.compact()
		if len(storage.palette.values) == 1 && storage.palette.values[0] == sub.air {
			// If the palette has only air in it, it means the storage is empty, so we can ignore it.
			continue
		}
		newStorages = append(newStorages, storage)
	}
	sub.storages = newStorages
}
