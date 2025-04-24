import struct, nbtlib
from io import BytesIO
from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_c_string, as_python_string
from ..utils import marshalNBT, unmarshalNBT


LIB.NewBedrockWorld.argtypes = [CString]
LIB.ReleaseBedrockWorld.argtypes = [CInt]
LIB.World_CloseWorld.argtypes = [CInt]
LIB.World_GetLevelDat.argtypes = [CInt]
LIB.World_ModifyLevelDat.argtypes = [CInt, CSlice]
LIB.LoadBiomes.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveBiomes.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.LoadChunkPayloadOnly.argtypes = [CInt, CInt, CInt, CInt]
LIB.LoadChunk.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveChunkPayloadOnly.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.SaveChunk.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.LoadSubChunk.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.SaveSubChunk.argtypes = [CInt, CInt, CInt, CInt, CInt, CInt]
LIB.LoadNBTPayloadOnly.argtypes = [CInt, CInt, CInt, CInt]
LIB.LoadNBT.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveNBTPayloadOnly.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.SaveNBT.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.LoadDeltaUpdate.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveDeltaUpdate.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.LoadTimeStamp.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveTimeStamp.argtypes = [CInt, CInt, CInt, CInt, CLongLong]
LIB.LoadDeltaUpdateTimeStamp.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveDeltaUpdateTimeStamp.argtypes = [CInt, CInt, CInt, CInt, CLongLong]
LIB.LoadFullSubChunkBlobHash.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveFullSubChunkBlobHash.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.LoadSubChunkBlobHash.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.SaveSubChunkBlobHash.argtypes = [CInt, CInt, CInt, CInt, CInt, CLongLong]

LIB.NewBedrockWorld.restype = CInt
LIB.ReleaseBedrockWorld.restype = None
LIB.World_CloseWorld.restype = CString
LIB.World_GetLevelDat.restype = CSlice
LIB.World_ModifyLevelDat.restype = CString
LIB.LoadBiomes.restype = CSlice
LIB.SaveBiomes.restype = CString
LIB.LoadChunkPayloadOnly.restype = CSlice
LIB.LoadChunk.restype = CLongLong
LIB.SaveChunkPayloadOnly.restype = CString
LIB.SaveChunk.restype = CString
LIB.LoadSubChunk.restype = CInt
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
    LIB.ReleaseBedrockWorld(CInt(id))


def world_close_world(id: int) -> str:
    return as_python_string(LIB.World_CloseWorld(CInt(id)))


def world_get_level_dat(id: int) -> tuple[nbtlib.tag.Compound | None, bool]:
    payload = as_python_bytes(LIB.World_GetLevelDat(CInt(id)))
    if len(payload) == 0:
        return None, False

    level_dat_data, _ = unmarshalNBT.UnMarshalBufferToPythonNBTObject(BytesIO(payload))
    return level_dat_data, True  # type: ignore


def world_modify_level_dat(id: int, level_dat: nbtlib.tag.Compound) -> str:
    writer = BytesIO()
    marshalNBT.MarshalPythonNBTObjectToWriter(writer, level_dat, "")
    return as_python_string(
        LIB.World_ModifyLevelDat(CInt(id), as_c_bytes(writer.getvalue()))
    )


def load_biomes(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(LIB.LoadBiomes(CInt(id), CInt(dm), CInt(x), CInt(z)))


def save_biomes(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveBiomes(CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload))
    )


def load_chunk_payload_only(id: int, dm: int, x: int, z: int) -> list[bytes]:
    payload = as_python_bytes(
        LIB.LoadChunkPayloadOnly(CInt(id), CInt(dm), CInt(x), CInt(z))
    )
    result = []

    ptr = 0
    while ptr < len(payload):
        l: int = struct.unpack("<I", payload[ptr : ptr + 4])[0]
        result.append(payload[ptr + 4 : ptr + 4 + l])
        ptr = ptr + 4 + l

    return result


def load_chunk(id: int, dm: int, x: int, z: int) -> tuple[int, int, int]:
    result = int(LIB.LoadChunk(CInt(id), CInt(dm), CInt(x), CInt(z)))
    return (
        (result & 1023) - 512,
        ((result >> 10) & 1023) - 512,
        result >> 20,
    )


def save_chunk_payload_only(
    id: int, dm: int, x: int, z: int, payload: list[bytes]
) -> str:
    writer = BytesIO()

    for i in payload:
        l = struct.pack("<I", len(i))
        writer.write(l)
        writer.write(i)

    return as_python_string(
        LIB.SaveChunkPayloadOnly(
            CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue())
        )
    )


def save_chunk(id: int, dm: int, x: int, z: int, chunk_id: int) -> str:
    return as_python_string(
        LIB.SaveChunk(CInt(id), CInt(dm), CInt(x), CInt(z), CInt(chunk_id))
    )


def load_sub_chunk(
    id: int,
    dm: int,
    x: int,
    y: int,
    z: int,
) -> int:
    return int(LIB.LoadSubChunk(CInt(id), CInt(dm), CInt(x), CInt(y), CInt(z)))


def save_sub_chunk(id: int, dm: int, x: int, y: int, z: int, sub_chunk_id: int) -> str:
    return as_python_string(
        LIB.SaveSubChunk(
            CInt(id), CInt(dm), CInt(x), CInt(y), CInt(z), CInt(sub_chunk_id)
        )
    )


def load_nbt_payload_only(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(LIB.LoadNBTPayloadOnly(CInt(id), CInt(dm), CInt(x), CInt(z)))


def load_nbt(id: int, dm: int, x: int, z: int) -> list[nbtlib.tag.Compound]:
    payload = as_python_bytes(LIB.LoadNBT(CInt(id), CInt(dm), CInt(x), CInt(z)))
    result = []

    ptr = 0
    while ptr < len(payload):
        l: int = struct.unpack("<I", payload[ptr : ptr + 4])[0]
        result.append(
            unmarshalNBT.UnMarshalBufferToPythonNBTObject(
                BytesIO(payload[ptr + 4 : ptr + 4 + l])
            )[0]
        )
        ptr = ptr + 4 + l

    return result


def save_nbt_payload_only(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveNBTPayloadOnly(
            CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload)
        )
    )


def save_nbt(id: int, dm: int, x: int, z: int, nbts: list[nbtlib.tag.Compound]) -> str:
    writer = BytesIO()

    for i in nbts:
        w = BytesIO()
        marshalNBT.MarshalPythonNBTObjectToWriter(w, i, "")

        binary_nbt = w.getvalue()
        l = struct.pack("<I", len(binary_nbt))

        writer.write(l)
        writer.write(binary_nbt)

    return as_python_string(
        LIB.SaveNBT(CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue()))
    )


def load_delta_update(id: int, dm: int, x: int, z: int) -> bytes:
    return as_python_bytes(LIB.LoadDeltaUpdate(CInt(id), CInt(dm), CInt(x), CInt(z)))


def save_delta_update(id: int, dm: int, x: int, z: int, payload: bytes) -> str:
    return as_python_string(
        LIB.SaveDeltaUpdate(CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(payload))
    )


def load_time_stamp(id: int, dm: int, x: int, z: int) -> int:
    return int(LIB.LoadTimeStamp(CInt(id), CInt(dm), CInt(x), CInt(z)))


def save_time_stamp(id: int, dm: int, x: int, z: int, time_stamp: int) -> str:
    return as_python_string(
        LIB.SaveTimeStamp(CInt(id), CInt(dm), CInt(x), CInt(z), CLongLong(time_stamp))
    )


def load_delta_update_time_stamp(id: int, dm: int, x: int, z: int) -> int:
    return int(LIB.LoadDeltaUpdateTimeStamp(CInt(id), CInt(dm), CInt(x), CInt(z)))


def save_delta_update_time_stamp(
    id: int, dm: int, x: int, z: int, time_stamp: int
) -> str:
    return as_python_string(
        LIB.SaveDeltaUpdateTimeStamp(
            CInt(id), CInt(dm), CInt(x), CInt(z), CLongLong(time_stamp)
        )
    )


def load_full_sub_chunk_blob_hash(
    id: int, dm: int, x: int, z: int
) -> list[tuple[int, int]]:
    payload = as_python_bytes(
        LIB.LoadFullSubChunkBlobHash(CInt(id), CInt(dm), CInt(x), CInt(z))
    )
    result = []

    ptr = 0
    while ptr < len(payload):
        result.append(
            (payload[ptr], struct.unpack("<Q", payload[ptr + 1 : ptr + 9])[0])
        )
        ptr += 9

    return result


def save_full_sub_chunk_blob_hash(
    id: int, dm: int, x: int, z: int, hashes: list[tuple[int, int]]
) -> str:
    writer = BytesIO()

    for i in hashes:
        writer.write(i[0].to_bytes())
        writer.write(struct.pack("<Q", i[1]))

    return as_python_string(
        LIB.SaveFullSubChunkBlobHash(
            CInt(id), CInt(dm), CInt(x), CInt(z), as_c_bytes(writer.getvalue())
        )
    )


def load_sub_chunk_blob_hash(id: int, dm: int, x: int, y: int, z: int) -> int:
    return int(LIB.LoadSubChunkBlobHash(CInt(id), CInt(dm), CInt(x), CInt(y), CInt(z)))


def save_sub_chunk_blob_hash(
    id: int, dm: int, x: int, y: int, z: int, hash: int
) -> str:
    return as_python_string(
        LIB.SaveSubChunkBlobHash(
            CInt(id), CInt(dm), CInt(x), CInt(y), CInt(z), CLongLong(hash)
        )
    )
