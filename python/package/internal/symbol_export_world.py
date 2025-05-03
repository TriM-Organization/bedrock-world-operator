import struct
import nbtlib
from io import BytesIO
from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_c_string, as_python_string
from ..utils import marshalNBT, unmarshalNBT


LIB.NewBedrockWorld.argtypes = [CString]
LIB.ReleaseBedrockWorld.argtypes = [CLongLong]
LIB.World_CloseWorld.argtypes = [CLongLong]
LIB.World_GetLevelDat.argtypes = [CLongLong]
LIB.World_ModifyLevelDat.argtypes = [CLongLong, CSlice]
LIB.LoadBiomes.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveBiomes.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.LoadChunkPayloadOnly.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.LoadChunk.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveChunkPayloadOnly.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.SaveChunk.argtypes = [CLongLong, CInt, CInt, CInt, CLongLong]
LIB.LoadSubChunk.argtypes = [CLongLong, CInt, CInt, CInt, CInt]
LIB.SaveSubChunk.argtypes = [CLongLong, CInt, CInt, CInt, CInt, CLongLong]
LIB.LoadNBTPayloadOnly.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.LoadNBT.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveNBTPayloadOnly.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.SaveNBT.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.LoadDeltaUpdate.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveDeltaUpdate.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.LoadTimeStamp.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveTimeStamp.argtypes = [CLongLong, CInt, CInt, CInt, CLongLong]
LIB.LoadDeltaUpdateTimeStamp.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveDeltaUpdateTimeStamp.argtypes = [CLongLong, CInt, CInt, CInt, CLongLong]
LIB.LoadFullSubChunkBlobHash.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.SaveFullSubChunkBlobHash.argtypes = [CLongLong, CInt, CInt, CInt, CSlice]
LIB.LoadSubChunkBlobHash.argtypes = [CLongLong, CInt, CInt, CInt, CInt]
LIB.SaveSubChunkBlobHash.argtypes = [CLongLong, CInt, CInt, CInt, CInt, CLongLong]

LIB.NewBedrockWorld.restype = CLongLong
LIB.ReleaseBedrockWorld.restype = None
LIB.World_CloseWorld.restype = CString
LIB.World_GetLevelDat.restype = CSlice
LIB.World_ModifyLevelDat.restype = CString
LIB.LoadBiomes.restype = CSlice
LIB.SaveBiomes.restype = CString
LIB.LoadChunkPayloadOnly.restype = CSlice
LIB.LoadChunk.restype = CSlice
LIB.SaveChunkPayloadOnly.restype = CString
LIB.SaveChunk.restype = CString
LIB.LoadSubChunk.restype = CLongLong
LIB.SaveSubChunk.restype = CString
LIB.LoadNBTPayloadOnly.restype = CSlice
LIB.LoadNBT.restype = CSlice
LIB.SaveNBTPayloadOnly.restype = CString
LIB.SaveNBT.restype = CString
LIB.LoadDeltaUpdate.restype = CSlice
LIB.SaveDeltaUpdate.restype = CString
LIB.LoadTimeStamp.restype = CLongLong
LIB.SaveTimeStamp.restype = CString
LIB.LoadDeltaUpdateTimeStamp.restype = CLongLong
LIB.SaveDeltaUpdateTimeStamp.restype = CString
LIB.LoadFullSubChunkBlobHash.restype = CSlice
LIB.SaveFullSubChunkBlobHash.restype = CString
LIB.LoadSubChunkBlobHash.restype = CLongLong
LIB.SaveSubChunkBlobHash.restype = CString


def new_bedrock_world(dir: str) -> int:
    return int(LIB.NewBedrockWorld(as_c_string(dir)))


def release_bedrock_world(id: int) -> None:
    LIB.ReleaseBedrockWorld(CLongLong(id))


def world_close_world(id: int) -> str:
    return as_python_string(LIB.World_CloseWorld(CLongLong(id)))


def world_get_level_dat(id: int) -> tuple[nbtlib.tag.Compound | None, bool]:
    payload = as_python_bytes(LIB.World_GetLevelDat(CLongLong(id)))
    if len(payload) == 0:
        return None, False

    level_dat_data, _ = unmarshalNBT.UnMarshalBufferToPythonNBTObject(BytesIO(payload))
    return level_dat_data, True  # type: ignore


def world_modify_level_dat(id: int, level_dat: nbtlib.tag.Compound) -> str:
    writer = BytesIO()
    marshalNBT.MarshalPythonNBTObjectToWriter(writer, level_dat, "")
    return as_python_string(
        LIB.World_ModifyLevelDat(CLongLong(id), as_c_bytes(writer.getvalue()))
    )


def load_biomes(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(LIB.LoadBiomes(CLongLong(id), CInt(dm), CInt(x), CInt(z)))


def save_biomes(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveBiomes(CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload))
    )


def load_chunk_payload_only(id: int, dm: int, x: int, z: int) -> list[bytes]:
    payload = as_python_bytes(
        LIB.LoadChunkPayloadOnly(CLongLong(id), CInt(dm), CInt(x), CInt(z))
    )
    result = []

    ptr = 0
    while ptr < len(payload):
        length: int = struct.unpack("<I", payload[ptr : ptr + 4])[0]
        result.append(payload[ptr + 4 : ptr + 4 + length])
        ptr = ptr + 4 + length

    return result


def load_chunk(id: int, dm: int, x: int, z: int) -> tuple[int, int, int]:
    result = as_python_bytes(LIB.LoadChunk(CLongLong(id), CInt(dm), CInt(x), CInt(z)))
    return struct.unpack("<hhQ", result)


def save_chunk_payload_only(
    id: int, dm: int, x: int, z: int, payload: list[bytes]
) -> str:
    writer = BytesIO()

    for i in payload:
        length = struct.pack("<I", len(i))
        writer.write(length)
        writer.write(i)

    return as_python_string(
        LIB.SaveChunkPayloadOnly(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue())
        )
    )


def save_chunk(id: int, dm: int, x: int, z: int, chunk_id: int) -> str:
    return as_python_string(
        LIB.SaveChunk(CLongLong(id), CInt(dm), CInt(x), CInt(z), CLongLong(chunk_id))
    )


def load_sub_chunk(
    id: int,
    dm: int,
    x: int,
    y: int,
    z: int,
) -> int:
    return int(LIB.LoadSubChunk(CLongLong(id), CInt(dm), CInt(x), CInt(y), CInt(z)))


def save_sub_chunk(id: int, dm: int, x: int, y: int, z: int, sub_chunk_id: int) -> str:
    return as_python_string(
        LIB.SaveSubChunk(
            CLongLong(id), CInt(dm), CInt(x), CInt(y), CInt(z), CLongLong(sub_chunk_id)
        )
    )


def load_nbt_payload_only(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(
        LIB.LoadNBTPayloadOnly(CLongLong(id), CInt(dm), CInt(x), CInt(z))
    )


def load_nbt(id: int, dm: int, x: int, z: int) -> list[nbtlib.tag.Compound]:
    payload = as_python_bytes(LIB.LoadNBT(CLongLong(id), CInt(dm), CInt(x), CInt(z)))
    result = []

    ptr = 0
    while ptr < len(payload):
        length: int = struct.unpack("<I", payload[ptr : ptr + 4])[0]
        result.append(
            unmarshalNBT.UnMarshalBufferToPythonNBTObject(
                BytesIO(payload[ptr + 4 : ptr + 4 + length])
            )[0]
        )
        ptr = ptr + 4 + length

    return result


def save_nbt_payload_only(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveNBTPayloadOnly(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload)
        )
    )


def save_nbt(id: int, dm: int, x: int, z: int, nbts: list[nbtlib.tag.Compound]) -> str:
    writer = BytesIO()

    for i in nbts:
        w = BytesIO()
        marshalNBT.MarshalPythonNBTObjectToWriter(w, i, "")

        binary_nbt = w.getvalue()
        length = struct.pack("<I", len(binary_nbt))

        writer.write(length)
        writer.write(binary_nbt)

    return as_python_string(
        LIB.SaveNBT(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue())
        )
    )


def load_delta_update(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(
        LIB.LoadDeltaUpdate(CLongLong(id), CInt(dm), CInt(x), CInt(z))
    )


def save_delta_update(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveDeltaUpdate(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload)
        )
    )


def load_time_stamp(id: int, dm: int, x: int, z: int) -> int:
    return int(LIB.LoadTimeStamp(CLongLong(id), CInt(dm), CInt(x), CInt(z)))


def save_time_stamp(id: int, dm: int, x: int, z: int, time_stamp: int) -> str:
    return as_python_string(
        LIB.SaveTimeStamp(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), CLongLong(time_stamp)
        )
    )


def load_delta_update_time_stamp(id: int, dm: int, x: int, z: int) -> int:
    return int(LIB.LoadDeltaUpdateTimeStamp(CLongLong(id), CInt(dm), CInt(x), CInt(z)))


def save_delta_update_time_stamp(
    id: int, dm: int, x: int, z: int, time_stamp: int
) -> str:
    return as_python_string(
        LIB.SaveDeltaUpdateTimeStamp(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), CLongLong(time_stamp)
        )
    )


def load_full_sub_chunk_blob_hash(
    id: int, dm: int, x: int, z: int
) -> list[tuple[int, int]]:
    payload = as_python_bytes(
        LIB.LoadFullSubChunkBlobHash(CLongLong(id), CInt(dm), CInt(x), CInt(z))
    )
    result = []

    ptr = 0
    while ptr < len(payload):
        result.append(struct.unpack("<bQ", payload[ptr : ptr + 9]))
        ptr += 9

    return result


def save_full_sub_chunk_blob_hash(
    id: int, dm: int, x: int, z: int, hashes: list[tuple[int, int]]
) -> str:
    writer = BytesIO()

    for i in hashes:
        writer.write(struct.pack("<bQ", i[0], i[1]))

    return as_python_string(
        LIB.SaveFullSubChunkBlobHash(
            CLongLong(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue())
        )
    )


def load_sub_chunk_blob_hash(id: int, dm: int, x: int, y: int, z: int) -> int:
    return int(
        LIB.LoadSubChunkBlobHash(CLongLong(id), CInt(dm), CInt(x), CInt(y), CInt(z))
    )


def save_sub_chunk_blob_hash(
    id: int, dm: int, x: int, y: int, z: int, hash: int
) -> str:
    return as_python_string(
        LIB.SaveSubChunkBlobHash(
            CLongLong(id), CInt(dm), CInt(x), CInt(y), CInt(z), CLongLong(hash)
        )
    )
