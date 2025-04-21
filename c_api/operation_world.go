package main

import "C"
import (
	"bytes"
	"encoding/binary"
	"fmt"

	"github.com/YingLunTown-DreamLand/bedrock-world-operator/define"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/world"
	"github.com/YingLunTown-DreamLand/bedrock-world-operator/world/leveldat"
	"github.com/sandertv/gophertunnel/minecraft/nbt"
)

var openedWorld = NewSimpleManager[world.World]()

//export NewBedrockWorld
func NewBedrockWorld(dirName *C.char) (id C.int) {
	w, err := world.Open(C.GoString(dirName))
	if err != nil {
		return -1
	}
	return C.int(openedWorld.AddObject(w))
}

//export ReleaseBedrockWorld
func ReleaseBedrockWorld(id C.int) {
	openedWorld.ReleaseObject(int(id))
}

//export World_CloseWorld
func World_CloseWorld(id C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("World_CloseWorld: World not found")
	}

	err := (*w).CloseWorld()
	if err != nil {
		return C.CString(fmt.Sprintf("World_CloseWorld: %v", err))
	}

	return C.CString("")
}

//export World_GetLevelDat
func World_GetLevelDat(id C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}

	dat := (*w).LevelDat()
	if dat == nil {
		return asCbytes(nil)
	}

	buf := bytes.NewBuffer(nil)
	nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian).Encode(dat)

	return asCbytes(buf.Bytes())
}

//export World_ModifyLevelDat
func World_ModifyLevelDat(id C.int, payload *C.char) *C.char {
	var dat leveldat.Data

	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("World_ModifyLevelDat: World not found")
	}

	err := nbt.NewDecoderWithEncoding(bytes.NewBuffer(asGoBytes(payload)), nbt.LittleEndian).Decode(&dat)
	if err != nil {
		return C.CString(fmt.Sprintf("World_ModifyLevelDat: %v", err))
	}

	*(*w).LevelDat() = dat
	err = (*w).UpdateLevelDat()
	if err != nil {
		return C.CString(fmt.Sprintf("World_ModifyLevelDat: %v", err))
	}

	return C.CString("")
}

//export LoadBiomes
func LoadBiomes(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}

	data, err := (*w).LoadBiomes(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})
	if err != nil {
		return asCbytes(nil)
	}

	return asCbytes(data)
}

//export SaveBiomes
func SaveBiomes(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveBiomes: World not found")
	}

	err := (*w).SaveBiomes(
		define.Dimension(dm),
		define.ChunkPos{int32(posx), int32(posz)},
		asGoBytes(payload),
	)
	if err != nil {
		return C.CString(fmt.Sprintf("SaveBiomes: %v", err))
	}

	return C.CString("")
}

//export LoadChunkPayloadOnly
func LoadChunkPayloadOnly(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	buf := bytes.NewBuffer(nil)

	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}

	subchunksBytes, _, _ := (*w).LoadChunkPayloadOnly(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})
	if len(subchunksBytes) == 0 {
		return asCbytes(nil)
	}

	for _, value := range subchunksBytes {
		l := make([]byte, 4)
		binary.LittleEndian.PutUint32(l, uint32(len(value)))
		_, _ = buf.Write(l)
		_, _ = buf.Write(value)
	}

	return asCbytes(buf.Bytes())
}

//export LoadChunk
func LoadChunk(id C.int, dm C.int, posx C.int, posz C.int) C.int {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}

	c, _, _ := (*w).LoadChunk(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})
	if c == nil {
		return -1
	}

	return C.int(savedChunk.AddObject(c))
}

//export SaveChunkPayloadOnly
func SaveChunkPayloadOnly(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) (err *C.char) {
	defer func() {
		r := recover()
		if r != nil {
			err = C.CString(fmt.Sprintf("SaveChunkPayloadOnly: %v", r))
		}
	}()

	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveChunkPayloadOnly: World not found")
	}

	goPayload := asGoBytes(payload)
	decodePayload := make([][]byte, 0)
	for len(goPayload) > 0 {
		l := binary.LittleEndian.Uint32(goPayload)
		decodePayload = append(decodePayload, goPayload[4:4+l])
		goPayload = goPayload[4+l:]
	}

	goErr := (*w).SaveChunkPayloadOnly(define.Dimension(dm), [2]int32{int32(posx), int32(posz)}, decodePayload)
	if goErr != nil {
		return C.CString(fmt.Sprintf("SaveChunkPayloadOnly: %v", goErr))
	}

	return C.CString("")
}

//export SaveChunk
func SaveChunk(id C.int, dm C.int, posx C.int, posz C.int, chunkID C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveChunk: World not found")
	}

	c := savedChunk.LoadObject(int(chunkID))
	if c == nil {
		return C.CString("SaveChunk: Found world but chunk not found")
	}

	err := (*w).SaveChunk(define.Dimension(dm), [2]int32{int32(posx), int32(posz)}, *c)
	if err != nil {
		return C.CString(fmt.Sprintf("SaveChunk: %v", err))
	}

	return C.CString("")
}

//export LoadSubChunk
func LoadSubChunk(id C.int, dm C.int, posx C.int, posy C.int, posz C.int) C.int {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}

	subChunk := (*w).LoadSubChunk(define.Dimension(dm), define.SubChunkPos{int32(posx), int32(posy), int32(posz)})
	if subChunk == nil {
		return -1
	}

	return C.int(savedSubChunk.AddObject(subChunk))
}

//export SaveSubChunk
func SaveSubChunk(id C.int, dm C.int, posx C.int, posy C.int, posz C.int, subChunkId C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveSubChunk: World not found")
	}

	subChunk := savedSubChunk.LoadObject(int(subChunkId))
	if subChunk == nil {
		return C.CString("SaveSubChunk: Found world but sub chunk not found")
	}

	err := (*w).SaveSubChunk(define.Dimension(dm), define.SubChunkPos{int32(posx), int32(posy), int32(posz)}, *subChunk)
	if err != nil {
		return C.CString(fmt.Sprintf("SaveSubChunk: %v", err))
	}

	return C.CString("")
}

//export LoadNBTPayloadOnly
func LoadNBTPayloadOnly(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}
	return asCbytes(
		(*w).LoadNBTPayloadOnly(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}),
	)
}

//export LoadNBT
func LoadNBT(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}

	nbts, err := (*w).LoadNBT(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})
	if err != nil {
		return asCbytes(nil)
	}

	result := make([]byte, 0)
	for _, value := range nbts {
		buf := bytes.NewBuffer(nil)
		_ = nbt.NewEncoderWithEncoding(buf, nbt.LittleEndian).Encode(value)

		l := make([]byte, 4)
		binary.LittleEndian.PutUint32(l, uint32(buf.Len()))

		if buf.Len() > 0 {
			result = append(result, l...)
			result = append(result, buf.Bytes()...)
		}
	}

	return asCbytes(result)
}

//export SaveNBTPayloadOnly
func SaveNBTPayloadOnly(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveNBTPayloadOnly: World not found")
	}

	err := (*w).SaveNBTPayloadOnly(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}, asGoBytes(payload))
	if err != nil {
		return C.CString(fmt.Sprintf("SaveNBTPayloadOnly: %v", err))
	}

	return C.CString("")
}

//export SaveNBT
func SaveNBT(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) (err *C.char) {
	defer func() {
		r := recover()
		if r != nil {
			err = C.CString(fmt.Sprintf("SaveNBT: %v", r))
		}
	}()

	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveNBT: World not found")
	}

	goPayload := asGoBytes(payload)
	nbts := make([]map[string]any, 0)
	for len(goPayload) > 0 {
		var decodeAns map[string]any

		l := binary.LittleEndian.Uint32(goPayload)
		_ = nbt.NewDecoderWithEncoding(bytes.NewBuffer(goPayload[4:4+l]), nbt.LittleEndian).Decode(&decodeAns)
		if len(decodeAns) > 0 {
			nbts = append(nbts, decodeAns)
		}

		goPayload = goPayload[4+l:]
	}

	goErr := (*w).SaveNBT(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}, nbts)
	if goErr != nil {
		return C.CString(fmt.Sprintf("SaveNBT: %v", goErr))
	}

	return C.CString("")
}

//export LoadDeltaUpdate
func LoadDeltaUpdate(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}
	data, _ := (*w).LoadDeltaUpdate(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})
	return asCbytes(data)
}

//export SaveDeltaUpdate
func SaveDeltaUpdate(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveDeltaUpdate: World not found")
	}

	goPayload := asGoBytes(payload)
	err := (*w).SaveDeltaUpdate(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}, goPayload)
	if err != nil {
		return C.CString(fmt.Sprintf("SaveDeltaUpdate: %v", err))
	}

	return C.CString("")
}

//export LoadTimeStamp
func LoadTimeStamp(id C.int, dm C.int, posx C.int, posz C.int) C.longlong {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}
	return C.longlong(
		(*w).LoadTimeStamp(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}),
	)
}

//export SaveTimeStamp
func SaveTimeStamp(id C.int, dm C.int, posx C.int, posz C.int, timeStamp C.longlong) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveTimeStamp: World not found")
	}

	err := (*w).SaveTimeStamp(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}, int64(timeStamp))
	if err != nil {
		return C.CString(fmt.Sprintf("SaveTimeStamp: %v", err))
	}

	return C.CString("")
}

//export LoadDeltaUpdateTimeStamp
func LoadDeltaUpdateTimeStamp(id C.int, dm C.int, posx C.int, posz C.int) C.longlong {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}
	return C.longlong(
		(*w).LoadDeltaUpdateTimeStamp(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}),
	)
}

//export SaveDeltaUpdateTimeStamp
func SaveDeltaUpdateTimeStamp(id C.int, dm C.int, posx C.int, posz C.int, timeStamp C.longlong) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveDeltaUpdateTimeStamp: World not found")
	}

	err := (*w).SaveDeltaUpdateTimeStamp(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)}, int64(timeStamp))
	if err != nil {
		return C.CString(fmt.Sprintf("SaveDeltaUpdateTimeStamp: %v", err))
	}

	return C.CString("")
}

//export LoadFullSubChunkBlobHash
func LoadFullSubChunkBlobHash(id C.int, dm C.int, posx C.int, posz C.int) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return asCbytes(nil)
	}

	result := make([]byte, 0)
	hashes := (*w).LoadFullSubChunkBlobHash(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posz)})

	for _, value := range hashes {
		hashBytes := make([]byte, 8)
		binary.LittleEndian.PutUint64(hashBytes, value.Hash)
		result = append(result, byte(value.PosY))
		result = append(result, hashBytes...)
	}

	return asCbytes(result)
}

//export SaveFullSubChunkBlobHash
func SaveFullSubChunkBlobHash(id C.int, dm C.int, posx C.int, posz C.int, payload *C.char) (err *C.char) {
	defer func() {
		r := recover()
		if r != nil {
			err = C.CString(fmt.Sprintf("SaveFullSubChunkBlobHash: %v", r))
		}
	}()

	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveFullSubChunkBlobHash: World not found")
	}

	hashes := make([]define.HashWithPosY, 0)
	payloadGoBytes := asGoBytes(payload)

	for len(payloadGoBytes) > 0 {
		hashes = append(hashes, define.HashWithPosY{
			PosY: int8(payloadGoBytes[0]),
			Hash: binary.LittleEndian.Uint64(payloadGoBytes[1:9]),
		})
		payloadGoBytes = payloadGoBytes[9:]
	}

	goError := (*w).SaveFullSubChunkBlobHash(define.Dimension(dm), define.ChunkPos{int32(posx), int32(posx)}, hashes)
	if goError != nil {
		return C.CString(fmt.Sprintf("SaveFullSubChunkBlobHash: %v", err))
	}

	return C.CString("")
}

//export LoadSubChunkBlobHash
func LoadSubChunkBlobHash(id C.int, dm C.int, posx C.int, posy C.int, posz C.int) C.longlong {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return -1
	}

	hash, found := (*w).LoadSubChunkBlobHash(define.Dimension(dm), define.SubChunkPos{int32(posx), int32(posy), int32(posz)})
	if !found {
		return -1
	}

	return C.longlong(hash)
}

//export SaveSubChunkBlobHash
func SaveSubChunkBlobHash(id C.int, dm C.int, posx C.int, posy C.int, posz C.int, hash C.longlong) *C.char {
	w := openedWorld.LoadObject(int(id))
	if w == nil {
		return C.CString("SaveSubChunkBlobHash: World not found")
	}

	err := (*w).SaveSubChunkBlobHash(define.Dimension(dm), define.SubChunkPos{int32(posx), int32(posy), int32(posz)}, uint64(hash))
	if err != nil {
		return C.CString(fmt.Sprintf("SaveSubChunkBlobHash: %v", err))
	}

	return C.CString("")
}
