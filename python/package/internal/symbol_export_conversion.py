import struct
from io import BytesIO
from .types import LIB
from .types import CSlice, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes


LIB.SubChunkNetworkPayload.argtypes = [CLongLong, CLongLong, CInt, CInt, CInt]
LIB.FromSubChunkNetworkPayload.argtypes = [CLongLong, CInt, CInt, CSlice]
LIB.SubChunkDiskPayload.argtypes = [CLongLong, CLongLong, CInt, CInt, CInt]
LIB.FromSubChunkDiskPayload.argtypes = [CLongLong, CInt, CInt, CSlice]

LIB.SubChunkNetworkPayload.restype = CSlice
LIB.FromSubChunkNetworkPayload.restype = CSlice
LIB.SubChunkDiskPayload.restype = CSlice
LIB.FromSubChunkDiskPayload.restype = CSlice


def sub_chunk_network_payload(
    sub_chunk_id: int, block_table_id: int, range_start: int, range_end: int, ind: int
) -> bytes:
    return as_python_bytes(
        LIB.SubChunkNetworkPayload(
            CLongLong(sub_chunk_id),
            CLongLong(block_table_id),
            CInt(range_start),
            CInt(range_end),
            CInt(ind),
        )
    )


def from_sub_chunk_network_payload(
    block_table_id: int, range_start: int, range_end: int, payload: bytes
) -> tuple[int, int, bool]:
    reader = BytesIO(
        as_python_bytes(
            LIB.FromSubChunkNetworkPayload(
                CLongLong(block_table_id),
                CInt(range_start),
                CInt(range_end),
                as_c_bytes(payload),
            )
        )
    )

    if reader.read(1) == b"\x00":
        return 0, 0, False

    index = reader.read(1)[0]
    sub_chunk_id = struct.unpack("<Q", reader.read(8))[0]

    return index, sub_chunk_id, True


def sub_chunk_disk_payload(
    sub_chunk_id: int, block_table_id: int, range_start: int, range_end: int, ind: int
) -> bytes:
    return as_python_bytes(
        LIB.SubChunkDiskPayload(
            CLongLong(sub_chunk_id),
            CLongLong(block_table_id),
            CInt(range_start),
            CInt(range_end),
            CInt(ind),
        )
    )


def from_sub_chunk_disk_payload(
    block_table_id: int, range_start: int, range_end: int, payload: bytes
) -> tuple[int, int, bool]:
    reader = BytesIO(
        as_python_bytes(
            LIB.FromSubChunkDiskPayload(
                CLongLong(block_table_id),
                CInt(range_start),
                CInt(range_end),
                as_c_bytes(payload),
            )
        )
    )

    if reader.read(1) == b"\x00":
        return 0, 0, False

    index = reader.read(1)[0]
    sub_chunk_id = struct.unpack("<Q", reader.read(8))[0]

    return index, sub_chunk_id, True
