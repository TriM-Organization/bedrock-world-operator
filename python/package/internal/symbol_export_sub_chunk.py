import numpy
from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_python_string


LIB.NewSubChunk.argtypes = []
LIB.ReleaseSubChunk.argtypes = [CLongLong]
LIB.SubChunk_Block.argtypes = [CLongLong, CInt, CInt, CInt, CInt]
LIB.SubChunk_Blocks.argtypes = [CLongLong, CInt]
LIB.SubChunk_Empty.argtypes = [CLongLong]
LIB.SubChunk_Equals.argtypes = [CLongLong, CLongLong]
LIB.SubChunk_SetBlock.argtypes = [CLongLong, CInt, CInt, CInt, CInt, CInt]
LIB.SubChunk_SetBlocks.argtypes = [CLongLong, CInt, CSlice]

LIB.NewSubChunk.restype = CLongLong
LIB.ReleaseSubChunk.restype = None
LIB.SubChunk_Block.restype = CInt
LIB.SubChunk_Blocks.restype = CSlice
LIB.SubChunk_Empty.restype = CInt
LIB.SubChunk_Equals.restype = CInt
LIB.SubChunk_SetBlock.restype = CString
LIB.SubChunk_SetBlocks.restype = CString


def new_sub_chunk() -> int:
    return int(LIB.NewSubChunk())


def release_sub_chunk(id: int) -> None:
    LIB.ReleaseSubChunk(CLongLong(id))


def sub_chunk_block(id: int, x: int, y: int, z: int, layer: int) -> int:
    return int(
        LIB.SubChunk_Block(CLongLong(id), CInt(x), CInt(y), CInt(z), CInt(layer))
    )


def sub_chunk_blocks(id: int, layer: int) -> numpy.ndarray:
    return numpy.frombuffer(
        as_python_bytes(LIB.SubChunk_Blocks(CLongLong(id), CInt(layer))), dtype="<u4"
    ).copy()


def sub_chunk_empty(id: int) -> int:
    return int(LIB.SubChunk_Empty(CLongLong(id)))


def sub_chunk_equals(id: int, another_sub_chunk_id: int) -> int:
    return int(LIB.SubChunk_Equals(CLongLong(id), CLongLong(another_sub_chunk_id)))


def sub_chunk_set_block(
    id: int, x: int, y: int, z: int, layer: int, block_runtime_id: int
) -> str:
    return as_python_string(
        LIB.SubChunk_SetBlock(
            CLongLong(id),
            CInt(x),
            CInt(y),
            CInt(z),
            CInt(layer),
            CInt(block_runtime_id),
        )
    )


def sub_chunk_set_blocks(id: int, layer: int, blocks: numpy.ndarray) -> str:
    return as_python_string(
        LIB.SubChunk_SetBlocks(CLongLong(id), CInt(layer), as_c_bytes(blocks.tobytes()))
    )
