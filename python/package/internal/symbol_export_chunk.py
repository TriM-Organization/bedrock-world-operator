import struct, numpy
from .types import LIB, CLongLong
from .types import CSlice, CString, CInt
from .types import as_c_bytes, as_python_bytes, as_python_string


LIB.NewChunk.argtypes = [CInt, CInt]
LIB.ReleaseChunk.argtypes = [CInt]
LIB.Chunk_Biome.argtypes = [CInt, CInt, CInt, CInt]
LIB.Chunk_Block.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_Blocks.argtypes = [CInt, CInt]
LIB.Chunk_Compact.argtypes = [CInt]
LIB.Chunk_Equals.argtypes = [CInt, CInt]
LIB.Chunk_HighestFilledSubChunk.argtypes = [CInt]
LIB.Chunk_SetBiome.argtypes = [CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_SetBlock.argtypes = [CInt, CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_SetBlocks.argtypes = [CInt, CInt, CSlice]
LIB.Chunk_Sub.argtypes = [CInt]
LIB.Chunk_SubChunk.argtypes = [CInt, CInt]

LIB.NewChunk.restype = CLongLong
LIB.ReleaseChunk.restype = None
LIB.Chunk_Biome.restype = CInt
LIB.Chunk_Block.restype = CInt
LIB.Chunk_Blocks.restype = CSlice
LIB.Chunk_Compact.restype = CString
LIB.Chunk_Equals.restype = CInt
LIB.Chunk_HighestFilledSubChunk.restype = CInt
LIB.Chunk_SetBiome.restype = CString
LIB.Chunk_SetBlock.restype = CString
LIB.Chunk_SetBlocks.restype = CString
LIB.Chunk_Sub.restype = CSlice
LIB.Chunk_SubChunk.restype = CInt


def new_chunk(range_start: int, range_end: int) -> tuple[int, int, int]:
    result = int(LIB.NewChunk(CInt(range_start), CInt(range_end)))
    return (
        (result & 1023) - 512,
        ((result >> 10) & 1023) - 512,
        result >> 20,
    )


def release_chunk(id: int) -> None:
    LIB.ReleaseChunk(CInt(id))


def chunk_biome(id: int, x: int, y: int, z: int) -> int:
    return int(LIB.Chunk_Biome(CInt(id), CInt(x), CInt(y), CInt(z)))


def chunk_block(id: int, x: int, y: int, z: int, layer: int) -> int:
    return int(LIB.Chunk_Block(CInt(id), CInt(x), CInt(y), CInt(z), CInt(layer)))


def chunk_blocks(id: int, layer: int) -> numpy.ndarray:
    return numpy.frombuffer(
        as_python_bytes(LIB.Chunk_Blocks(CInt(id), CInt(layer))), dtype=numpy.uint32
    ).copy()


def chunk_compact(id: int) -> str:
    return as_python_string(LIB.Chunk_Compact(CInt(id)))


def chunk_equals(id: int, another_chunk_id: int) -> int:
    return int(LIB.Chunk_Equals(CInt(id), CInt(another_chunk_id)))


def chunk_highest_filled_sub_chunk(id: int) -> int:
    return int(LIB.Chunk_HighestFilledSubChunk(CInt(id)))


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


def chunk_set_blocks(id: int, layer: int, blocks: numpy.ndarray) -> str:
    return as_python_string(
        LIB.Chunk_SetBlocks(CInt(id), CInt(layer), as_c_bytes(blocks.tobytes()))
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
