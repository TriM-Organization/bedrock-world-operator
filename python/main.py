import ctypes
import struct

LIB = ctypes.cdll.LoadLibrary("python/out.dll")

CPtr = ctypes.c_void_p
CSlice = CPtr
CString = ctypes.c_char_p
CInt = ctypes.c_int
CLongLong = ctypes.c_longlong


def as_c_bytes(b: bytes) -> ctypes.c_char_p:
    return ctypes.c_char_p(struct.pack("<I", len(b)) + b)


def as_python_bytes(slice: CSlice) -> bytes:
    l = struct.unpack("<I", ctypes.string_at(slice, 4))[0]
    return ctypes.string_at(slice, 4 + l)[4:]


def as_c_string(string: str) -> CString:
    return CString(bytes(string, encoding="utf-8"))


def as_python_string(c_string: bytes) -> str:
    if c_string is None:
        return ""
    return c_string.decode(encoding="utf-8")


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
    return LIB.SubChunk_SetBlock(
        CInt(id), CInt(x), CInt(y), CInt(z), CInt(layer), CInt(block_runtime_id)
    )
