from .constant import RANGE_OVERWORLD
from .define import Range
from ..world.sub_chunk import SubChunk, SubChunkWithIndex
from ..world.block_table import BlockTable
from ..internal.symbol_export_conversion import (
    sub_chunk_network_payload as scnp,
    from_sub_chunk_network_payload as fscnp,
    sub_chunk_disk_payload as scdp,
    from_sub_chunk_disk_payload as fscdp,
)


def sub_chunk_network_payload(
    sub_chunk: SubChunk, block_table: BlockTable, index: int, r: Range = RANGE_OVERWORLD
) -> bytes:
    """
    sub_chunk_network_payload encodes sub_chunk to its
    payload represent that could use on network sending.

    Args:
        sub_chunk (SubChunk): The sub chunk want to encode.
        block_table (BlockTable): The block runtime ID table that used to encode this sub chunk.
        index (int): The index of this sub chunk, and must be bigger than -1.
                     For example, for a block in (x, -63, z), then its
                     sub chunk Y pos will be -63>>4 (-4).
                     However, this is not the index of this sub chunk,
                     we need to do other compute to get the index:
                     index = (-63>>4) - (r.start_range>>4)
                           = (-63>>4) - (-64>>4)
                           = 0
        r (Range, optional): The whole chunk range where this sub chunk is in.
                             For Overworld, the range of it is Range(-64, 319).
                             Defaults to RANGE_OVERWORLD.


    Returns:
        bytes: The bytes represent of this sub chunk, and could especially send on network.
               Therefore, this is a Network encoding sub chunk payload.
    """
    return scnp(
        sub_chunk._sub_chunk_id,
        block_table._table_id,
        r.start_range,
        r.end_range,
        index,
    )


def from_sub_chunk_network_payload(
    block_table: BlockTable, payload: bytes, r: Range = RANGE_OVERWORLD
) -> SubChunkWithIndex:
    """
    from_sub_chunk_network_payload decoding a Network
    encoding sub chunk and return its python represent.

    Args:
        block_table (BlockTable): The block runtime ID table that used to decode this sub chunk.
        payload (bytes): The bytes of this sub chunk, who with a Network encoding.
        r (Range, optional): The whole chunk range where this sub chunk is in.
                             For Overworld, it is Range(-64, 319).
                             Defaults to RANGE_OVERWORLD.

    Returns:
        SubChunkWithIndex:
            If failed to decode, then return an invalid sub chunk and an invalid -1 sub chunk Y index.
            Otherwise, return decoded sub chunk with its Y index.
            Note that you could use s.sub_chunk.is_valid() to check whether the sub chunk is valid or not.
    """
    s = SubChunkWithIndex(-1)
    index, sub_chunk_id, success = fscnp(
        block_table._table_id, r.start_range, r.end_range, payload
    )
    if not success:
        return s
    s.index, s.sub_chunk._sub_chunk_id = index, sub_chunk_id
    return s


def sub_chunk_disk_payload(
    sub_chunk: SubChunk, block_table: BlockTable, index: int, r: Range = RANGE_OVERWORLD
) -> bytes:
    """
    sub_chunk_disk_payload encodes sub_chunk to
    its payload represent under Disk encoding.

    That means the returned bytes could save it
    to disk if it is bigger than 0.

    Args:
        sub_chunk (SubChunk): The sub chunk want to encode.
        block_table (BlockTable): The block runtime ID table that used to encode this sub chunk.
        index (int): The index of this sub chunk, and must be bigger than -1.
                     For example, for a block in (x, -63, z), then its
                     sub chunk Y pos will be -63>>4 (-4).
                     However, this is not the index of this sub chunk,
                     we need to do other compute to get the index:
                     index = (-63>>4) - (r.start_range>>4)
                           = (-63>>4) - (-64>>4)
                           = 0
        r (Range, optional): The whole chunk range where this sub chunk is in.
                             For Overworld, it is Range(-64, 319).
                             Defaults to RANGE_OVERWORLD.


    Returns:
        bytes: The bytes represent of this sub chunk, who with a Disk encoding.
    """
    return scdp(
        sub_chunk._sub_chunk_id,
        block_table._table_id,
        r.start_range,
        r.end_range,
        index,
    )


def from_sub_chunk_disk_payload(
    block_table: BlockTable, payload: bytes, r: Range = RANGE_OVERWORLD
) -> SubChunkWithIndex:
    """
    from_sub_chunk_disk_payload decoding a Disk encoding
    sub chunk and return its python represent.

    Args:
        block_table (BlockTable): The block runtime ID table that used to decode this sub chunk.
        payload (bytes): The bytes of this sub chunk, who with a Disk encoding.
        r (Range, optional): The whole chunk range where this sub chunk is in.
                             For Overworld, the range of it is Range(-64, 319).
                             Defaults to RANGE_OVERWORLD.

    Returns:
        SubChunkWithIndex:
            If failed to decode, then return an invalid sub chunk and an invalid -1 sub chunk Y index.
            Otherwise, return decoded sub chunk with its Y index.
            Note that you could use s.sub_chunk.is_valid() to check whether the sub chunk is valid or not.
    """
    s = SubChunkWithIndex(-1)
    index, sub_chunk_id, success = fscdp(
        block_table._table_id, r.start_range, r.end_range, payload
    )
    if not success:
        return s
    s.index, s.sub_chunk._sub_chunk_id = index, sub_chunk_id
    return s
