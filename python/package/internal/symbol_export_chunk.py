from io import BytesIO
import struct
import numpy
from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_python_string


LIB.NewChunk.argtypes = [CInt, CInt]
LIB.ReleaseChunk.argtypes = [CLongLong]
LIB.Chunk_Biome.argtypes = [CLongLong, CInt, CInt, CInt]
LIB.Chunk_Biomes.argtypes = [CLongLong]
LIB.Chunk_Block.argtypes = [CLongLong, CInt, CInt, CInt, CInt]
LIB.Chunk_Blocks.argtypes = [CLongLong, CInt]
LIB.Chunk_Compact.argtypes = [CLongLong]
LIB.Chunk_Equals.argtypes = [CLongLong, CLongLong]
LIB.Chunk_HighestFilledSubChunk.argtypes = [CLongLong]
LIB.Chunk_SetBiome.argtypes = [CLongLong, CInt, CInt, CInt, CInt]
LIB.Chunk_SetBiomes.argtypes = [CLongLong, CSlice]
LIB.Chunk_SetBlock.argtypes = [CLongLong, CInt, CInt, CInt, CInt, CInt]
LIB.Chunk_SetBlocks.argtypes = [CLongLong, CInt, CSlice]
LIB.Chunk_Sub.argtypes = [CLongLong]
LIB.Chunk_SetSub.argtypes = [CLongLong, CSlice]
LIB.Chunk_SubChunk.argtypes = [CLongLong, CInt]
LIB.Chunk_SetSubChunk.argtypes = [CLongLong, CLongLong, CInt]

LIB.NewChunk.restype = CSlice
LIB.ReleaseChunk.restype = None
LIB.Chunk_Biome.restype = CInt
LIB.Chunk_Biomes.restype = CSlice
LIB.Chunk_Block.restype = CInt
LIB.Chunk_Blocks.restype = CSlice
LIB.Chunk_Compact.restype = CString
LIB.Chunk_Equals.restype = CInt
LIB.Chunk_HighestFilledSubChunk.restype = CInt
LIB.Chunk_SetBiome.restype = CString
LIB.Chunk_SetBiomes.restype = CString
LIB.Chunk_SetBlock.restype = CString
LIB.Chunk_SetBlocks.restype = CString
LIB.Chunk_Sub.restype = CSlice
LIB.Chunk_SetSub.restype = CString
LIB.Chunk_SubChunk.restype = CLongLong
LIB.Chunk_SetSubChunk.restype = CString


def new_chunk(range_start: int, range_end: int) -> tuple[int, int, int]:
    result = as_python_bytes(LIB.NewChunk(CInt(range_start), CInt(range_end)))
    return struct.unpack("<hhQ", result)


def release_chunk(id: int) -> None:
    LIB.ReleaseChunk(CLongLong(id))


def chunk_biome(id: int, x: int, y: int, z: int) -> int:
    return int(LIB.Chunk_Biome(CLongLong(id), CInt(x), CInt(y), CInt(z)))


def chunk_biomes(id: int) -> numpy.ndarray:
    return numpy.frombuffer(
        as_python_bytes(LIB.Chunk_Biomes(CLongLong(id))), dtype="<u4"
    ).copy()


def chunk_block(id: int, x: int, y: int, z: int, layer: int) -> int:
    return int(LIB.Chunk_Block(CLongLong(id), CInt(x), CInt(y), CInt(z), CInt(layer)))


def chunk_blocks(id: int, layer: int) -> numpy.ndarray:
    return numpy.frombuffer(
        as_python_bytes(LIB.Chunk_Blocks(CLongLong(id), CInt(layer))), dtype="<u4"
    ).copy()


def chunk_compact(id: int) -> str:
    return as_python_string(LIB.Chunk_Compact(CLongLong(id)))


def chunk_equals(id: int, another_chunk_id: int) -> int:
    return int(LIB.Chunk_Equals(CLongLong(id), CLongLong(another_chunk_id)))


def chunk_highest_filled_sub_chunk(id: int) -> int:
    return int(LIB.Chunk_HighestFilledSubChunk(CLongLong(id)))


def chunk_set_biome(id: int, x: int, y: int, z: int, biome_id: int) -> str:
    return as_python_string(
        LIB.Chunk_SetBiome(CLongLong(id), CInt(x), CInt(y), CInt(z), CInt(biome_id))
    )


def chunk_set_biomes(id: int, blocks: numpy.ndarray) -> str:
    return as_python_string(
        LIB.Chunk_SetBiomes(CLongLong(id), as_c_bytes(blocks.tobytes()))
    )


def chunk_set_block(
    id: int, x: int, y: int, z: int, layer: int, block_runtime_id: int
) -> str:
    return as_python_string(
        LIB.Chunk_SetBlock(
            CLongLong(id),
            CInt(x),
            CInt(y),
            CInt(z),
            CInt(layer),
            CInt(block_runtime_id),
        )
    )


def chunk_set_blocks(id: int, layer: int, blocks: numpy.ndarray) -> str:
    return as_python_string(
        LIB.Chunk_SetBlocks(CLongLong(id), CInt(layer), as_c_bytes(blocks.tobytes()))
    )


def chunk_sub(id: int) -> list[int]:
    raw = as_python_bytes(LIB.Chunk_Sub(CLongLong(id)))
    result = []

    ptr = 0
    while ptr < len(raw):
        result.append(struct.unpack("<Q", raw[ptr : ptr + 8])[0])
        ptr += 8

    return result


def chunk_set_sub(id: int, sub_chunk_ids: list[int]) -> str:
    writer = BytesIO()
    for i in sub_chunk_ids:
        writer.write(struct.pack("<Q", i))
    return as_python_string(
        LIB.Chunk_SetSub(CLongLong(id), as_c_bytes(writer.getvalue()))
    )


def chunk_sub_chunk(id: int, y: int) -> int:
    return int(LIB.Chunk_SubChunk(CLongLong(id), CInt(y)))


def chunk_set_sub_chunk(id: int, sub_chunk_id: int, index: int) -> str:
    return as_python_string(
        LIB.Chunk_SetSubChunk(CLongLong(id), CLongLong(sub_chunk_id), CInt(index))
    )
