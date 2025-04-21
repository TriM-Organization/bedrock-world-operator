import ctypes, struct, nbtlib
from io import BytesIO
from .types import LIB
from .types import CPtr, CSlice, CString, CInt
from .types import as_c_bytes, as_python_bytes, as_c_string, as_python_string
from ..utils import marshalNBT, unmarshalNBT


LIB.FreeMemory.argtypes = [CPtr]
LIB.FreeMemory.restype = None


def free_memory(address: CPtr) -> None:
    LIB.FreeMemory(address)


LIB.NewChunk.argtypes = [CInt, CInt]
LIB.ReleaseChunk.argtypes = [CInt]
LIB.Chunk_Biome.argtypes = [CInt, CInt, CInt, CInt]
LIB.Chunk_Block.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_Compact.argtypes = [CInt]
LIB.Chunk_Equals.argtypes = [CInt, CInt]
LIB.Chunk_HighestFilledSubChunk.argtypes = [CInt]
LIB.Chunk_Range.argtypes = [CInt]
LIB.Chunk_SetBiome.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_SetBlock.argtypes = [CInt, CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_Sub.argtypes = [CInt]
LIB.Chunk_SubChunk.argtypes = [CInt, CInt]
LIB.Chunk_SubIndex.argtypes = [CInt, CInt]
LIB.Chunk_SubY.argtypes = [CInt, CInt]

LIB.NewChunk.restype = CInt
LIB.ReleaseChunk.restype = None
LIB.Chunk_Biome.restype = CInt
LIB.Chunk_Block.restype = CInt
LIB.Chunk_Compact.restype = CString
LIB.Chunk_Equals.restype = CInt
LIB.Chunk_HighestFilledSubChunk.restype = CInt
LIB.Chunk_Range.restype = CSlice
LIB.Chunk_SetBiome.restype = CString
LIB.Chunk_SetBlock.restype = CString
LIB.Chunk_Sub.restype = CSlice
LIB.Chunk_SubChunk.restype = CInt
LIB.Chunk_SubIndex.restype = CInt
LIB.Chunk_SubY.restype = CInt


def new_chunk(range_start: int, range_end: int) -> int:
    return int(LIB.NewChunk(CInt(range_start), CInt(range_end)))


def release_chunk(id: int) -> None:
    LIB.ReleaseChunk(CInt(id))


def chunk_biome(id: int, x: int, y: int, biome_id: int) -> int:
    return int(LIB.Chunk_Biome(CInt(id), CInt(x), CInt(y), CInt(y), CInt(biome_id)))


def chunk_block(id: int, x: int, y: int, z: int, layer: int) -> int:
    return int(LIB.Chunk_Block(CInt(id), CInt(x), CInt(y), CInt(z), CInt(layer)))


def chunk_compact(id: int) -> str:
    return as_python_string(LIB.Chunk_Compact(CInt(id)))


def chunk_equals(id: int, another_chunk_id: int) -> int:
    return int(LIB.Chunk_Equals(CInt(id), CInt(another_chunk_id)))


def chunk_highest_filled_sub_chunk(id: int) -> int:
    return int(LIB.Chunk_HighestFilledSubChunk(CInt(id)))


def chunk_range(id: int) -> tuple[int, int, bool]:
    data = as_python_bytes(LIB.Chunk_Range(CInt(id)))
    if len(data) == 0:
        return (0, 0, False)

    start_range = struct.unpack("<i", data[0:4])[0]
    end_range = struct.unpack("<i", data[4:])[0]

    return (start_range, end_range, True)


def chunk_set_biome(id: int, x: int, y: int, z: int, biome_id: int) -> str:
    return as_python_string(
        LIB.Chunk_SetBiome(CInt(id), CInt(x), CInt(y), CInt(z), CInt(biome_id))
    )


def chunk_set_block(
    id: int, x: int, y: int, z: int, layer: int, block_runtime_id: int
) -> str:
    return as_python_string(
        LIB.Chunk_SetBlock(
            CInt(id), CInt(x), CInt(y), CInt(z), CInt(layer), CInt(block_runtime_id)
        )
    )


def chunk_sub(id: int) -> list[int]:
    raw = as_python_bytes(LIB.Chunk_Sub(CInt(id)))
    result = []

    ptr = 0
    while ptr < len(raw):
        result.append(struct.unpack("<I", raw[ptr : ptr + 4])[0])
        ptr += 4

    return result


def chunk_sub_chunk(id: int, y: int) -> int:
    return int(LIB.Chunk_SubChunk(CInt(id), CInt(y)))


def chunk_sub_index(id: int, y: int) -> int:
    return int(LIB.Chunk_SubIndex(CInt(id), CInt(y)))


def chunk_sub_y(id: int, index: int) -> int:
    return int(LIB.Chunk_SubY(CInt(id), CInt(index)))


LIB.NewSubChunk.argtypes = [CInt, CInt]
LIB.ReleaseSubChunk.argtypes = [CInt]
LIB.SubChunk_Block.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.SubChunk_Empty.argtypes = [CInt]
LIB.SubChunk_Equals.argtypes = [CInt, CInt]
LIB.SubChunk_SetBlock.argtypes = [CInt, CInt, CInt, CInt, CInt, CInt]

LIB.NewSubChunk.restype = CInt
LIB.ReleaseSubChunk.restype = None
LIB.SubChunk_Block.restype = CInt
LIB.SubChunk_Empty.restype = CInt
LIB.SubChunk_Equals.restype = CInt
LIB.SubChunk_SetBlock.restype = None


def new_sub_chunk(range_start: int, range_end: int) -> int:
    return int(LIB.NewSubChunk(CInt(range_start), CInt(range_end)))


def release_sub_chunk(id: int) -> None:
    LIB.ReleaseSubChunk(CInt(id))


def sub_chunk_empty(id: int) -> int:
    return int(LIB.SubChunk_Empty(CInt(id)))


def sub_chunk_equals(id: int, another_sub_chunk_id: int) -> int:
    return int(LIB.SubChunk_Equals(CInt(id), CInt(another_sub_chunk_id)))


def sub_chunk_set_block(
    id: int, x: int, y: int, z: int, layer: int, block_runtime_id: int
) -> None:
    LIB.SubChunk_SetBlock(
        CInt(id), CInt(x), CInt(y), CInt(z), CInt(layer), CInt(block_runtime_id)
    )


LIB.NewBedrockWorld.argtypes = [CString]
LIB.ReleaseBedrockWorld.argtypes = [CInt]
LIB.World_Close.argtypes = [CInt]
LIB.World_GetLevelDat.argtypes = [CInt]
LIB.World_ModifyLevelDat.argtypes = [CInt, CSlice]
LIB.LoadBiomes.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveBiomes.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.LoadChunkPayloadOnly.argtypes = [CInt, CInt, CInt, CInt]
LIB.LoadChunk.argtypes = [CInt, CInt, CInt, CInt]
LIB.SaveChunkPayloadOnly.argtypes = [CInt, CInt, CInt, CInt, CSlice]
LIB.SaveChunk.argtypes = [CInt, CInt, CInt, CInt, CInt]

LIB.NewBedrockWorld.restype = CInt
LIB.ReleaseBedrockWorld.restype = None
LIB.World_Close.restype = CString
LIB.World_GetLevelDat.restype = CSlice
LIB.World_ModifyLevelDat.restype = CString
LIB.LoadBiomes.restype = CSlice
LIB.SaveBiomes.restype = CString
LIB.LoadChunkPayloadOnly.restype = CSlice
LIB.LoadChunk.restype = CInt
LIB.SaveChunkPayloadOnly.restype = CString
LIB.SaveChunk.restype = CString


def new_bedrock_world(dir: str) -> int:
    return int(LIB.NewBedrockWorld(as_c_string(dir)))


def release_bedrock_world(id: int) -> None:
    LIB.ReleaseBedrockWorld(CInt(id))


def world_close(id: int) -> str:
    return as_python_string(LIB.World_Close(CInt(id)))


def world_get_level_dat(id: int) -> tuple[nbtlib.tag.Compound | None, bool]:
    payload = as_python_bytes(LIB.World_GetLevelDat(CInt(id)))
    if len(payload) == 0:
        return (None, False)

    level_dat_data, _ = unmarshalNBT.UnMarshalBufferToPythonNBTObject(BytesIO(payload))
    return (level_dat_data, True)  # type: ignore


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


def load_chunk(id: int, dm: int, x: int, z: int) -> int:
    return int(LIB.LoadChunk(CInt(id), CInt(dm), CInt(x), CInt(z)))


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
