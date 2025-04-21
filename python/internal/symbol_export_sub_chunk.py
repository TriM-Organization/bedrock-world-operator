from .types import LIB
from .types import CInt


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
