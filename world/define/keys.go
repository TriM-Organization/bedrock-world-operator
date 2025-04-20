package world_define

import (
	"encoding/binary"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
)

//lint:file-ignore U1000 Unused unexported constants are present for future code using these.

// Keys on a per-sub chunk basis. These are prefixed by the chunk coordinates and subchunk ID.
const (
	KeySubChunkData = '/' // 2f
)

// Keys on a per-chunk basis. These are prefixed by only the chunk coordinates.
const (
	// keyVersion holds a single byte of data with the version of the chunk.
	KeyVersion = ',' // 2c
	// keyVersionOld was replaced by keyVersion. It is still used by vanilla to check compatibility, but vanilla no
	// longer writes this tag.
	KeyVersionOld = 'v' // 76
	// keyBlockEntities holds n amount of NBT compound tags appended to each other (not a TAG_List, just appended). The
	// compound tags contain the position of the block entities.
	KeyBlockEntities = '1' // 31
	// keyEntities holds n amount of NBT compound tags appended to each other (not a TAG_List, just appended). The
	// compound tags contain the position of the entities.
	KeyEntities = '2' // 32
	// keyFinalisation contains a single LE int32 that indicates the state of generation of the chunk. If 0, the chunk
	// needs to be ticked. If 1, the chunk needs to be populated and if 2 (which is the state generally found in world
	// saves from vanilla), the chunk is fully finalised.
	KeyFinalisation = '6' // 36
	// key3DData holds 3-dimensional biomes for the entire chunk.
	Key3DData = '+' // 2b
	// key2DData is no longer used in worlds with world height change. It was replaced by key3DData in newer worlds
	// which has 3-dimensional biomes.
	Key2DData = '-' // 2d
	// keyChecksum holds a list of checksums of some sort. It's not clear of what data this checksum is composed or what
	// these checksums are used for.
	KeyChecksums = ';' // 3b

	KeyEntityIdentifiers = "digp"
	KeyEntity            = "actorprefix"

	KeyChunkTimeStamp       = 'T'              // time stamp
	KeyDeltaUpdateTimeStamp = "dutsp"          // delta update time stamp prefix
	KeyDeltaUpdate          = "dup"            // delta update prefix
	KeyBlobHash             = "blobhashprefix" // blob hash prefix
)

// Keys on a per-world basis. These are found only once in a leveldb world save.
const (
	KeyAutonomousEntities = "AutonomousEntities"
	KeyOverworld          = "Overworld"
	KeyMobEvents          = "mobevents"
	KeyBiomeData          = "BiomeData"
	KeyScoreboard         = "scoreboard"
	KeyLocalPlayer        = "~local_player"
)

const (
	FinalisationGenerated = iota + 1
	FinalisationPopulated
)

// Index returns a byte buffer holding the written index of the chunk position passed. If the dimension passed to New
// is not world.Overworld, the length of the index returned is 12. It is 8 otherwise.
func Index(dm define.Dimension, position define.ChunkPos) []byte {
	x, z, dim := uint32(position[0]), uint32(position[1]), uint32(dm)
	b := make([]byte, 12)

	binary.LittleEndian.PutUint32(b, x)
	binary.LittleEndian.PutUint32(b[4:], z)
	if dim == 0 {
		return b[:8]
	}
	binary.LittleEndian.PutUint32(b[8:], dim)
	return b
}

// Sum converts Index(dm, position) to its []byte representation and appends p.
// Note that Sum is very necessary because all Sum do is preventing users from
// believing that "append" can create new slices (however, it not).
func Sum(dm define.Dimension, position define.ChunkPos, p ...byte) []byte {
	return append(Index(dm, position), p...)
}
