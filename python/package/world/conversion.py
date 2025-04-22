import nbtlib
from .define import BlockStates, Range
from ..world.sub_chunk import SubChunk, SubChunkWithIndex
from ..internal.symbol_export_conversion import (
    runtime_id_to_state as rits,
    state_to_runtime_id as stri,
    sub_chunk_network_payload as scnp,
    from_sub_chunk_network_payload as fscnp,
    sub_chunk_disk_payload as scdp,
    from_sub_chunk_disk_payload as fscdp,
)


def runtime_id_to_state(
    block_runtime_id: int,
) -> tuple[BlockStates | None, bool]:
    """runtime_id_to_state convert block runtime id to a BlockStates.

    Args:
        block_runtime_id (int): The runtime id of target block.

    Returns:
        tuple[BlockStates | None, bool]: If not found, return (None, False).
                                         Otherwise, return BlockStates and True.
    """
    name, states, success = rits(block_runtime_id)
    if not success:
        return (None, False)
    return (BlockStates(name, states), True)  # type: ignore


def state_to_runtime_id(
    block_name: str, block_states: nbtlib.tag.Compound
) -> tuple[int, bool]:
    """
    state_to_runtime_id convert a block which name is block_name
    and states is block_states to its block runtime id represent.

    Args:
        block_name (str): The name of this block.
        block_states (nbtlib.tag.Compound): The block states of this block.

    Returns:
        tuple[int, bool]: If not found, return (0, False).
                          Otherwise, return its block runtime id and True.
    """
    block_runtime_id, success = stri(block_name, block_states)
    if not success:
        return (0, False)
    return (block_runtime_id, True)


def sub_chunk_network_payload(sub_chunk: SubChunk, r: Range, index: int) -> bytes:
    """
    sub_chunk_network_payload encodes sub_chunk to its payload represent that could use on network sending.

    Args:
        sub_chunk (SubChunk): The sub chunk want to encode.
        r (Range): The whole chunk range where this sub chunk is in.
                   For overworld, it is Range(-64, 319).
        index (int): The index of this sub chunk, must bigger than -1.
                     For example, for a block in (x, -63, z), than its
                     sub chunk Y pos will be -63>>4 (-4).
                     However, this is not the index of this sub chunk,
                     we need do other compute to get the index:
                     index = (-63>>4) - (r.start_range>>4)
                           = (-63>>4) - (-64>>4)
                           = 0


    Returns:
        bytes: The bytes represent of this sub chunk, and could especially sending on network.
               Therefore, this is a Network encoding sub chunk payload.
    """
    return scnp(sub_chunk._sub_chunk_id, r.start_range, r.end_range, index)


def from_sub_chunk_network_payload(
    r: Range, payload: bytes
) -> tuple[SubChunkWithIndex | None, bool]:
    """from_sub_chunk_network_payload decode a Network encoding sub chunk and return its python represent.

    Args:
        r (Range): The whole chunk range where this sub chunk is in.
                   For overworld, it is Range(-64, 319).
        payload (bytes): The bytes of this sub chunk, who with a Network encoding.

    Returns:
        tuple[SubChunkWithIndex | None, bool]: If failed to decode, then return (None, False).
                                               Otherwise, return decoded sub chunk and True.
    """
    index, sub_chunk_id, success = fscnp(r.start_range, r.end_range, payload)
    if not success:
        return (None, False)
    s = SubChunk()
    s._sub_chunk_id = sub_chunk_id
    return (SubChunkWithIndex(index, s), True)


def sub_chunk_disk_payload(sub_chunk: SubChunk, r: Range, index: int) -> bytes:
    """
    sub_chunk_disk_payload encodes sub_chunk to its payload represent under Disk encoding.
    That means the returned bytes could save to disk if its len bigger than 0.

    Args:
        sub_chunk (SubChunk): The sub chunk want to encode.
        r (Range): The whole chunk range where this sub chunk is in.
                   For overworld, it is Range(-64, 319).
        index (int): The index of this sub chunk, must bigger than -1.
                     For example, for a block in (x, -63, z), than its
                     sub chunk Y pos will be -63>>4 (-4).
                     However, this is not the index of this sub chunk,
                     we need do other compute to get the index:
                     index = (-63>>4) - (r.start_range>>4)
                           = (-63>>4) - (-64>>4)
                           = 0


    Returns:
        bytes: The bytes represent of this sub chunk, who with a Disk encoding.
    """
    return scdp(sub_chunk._sub_chunk_id, r.start_range, r.end_range, index)


def from_sub_chunk_disk_payload(
    r: Range, payload: bytes
) -> tuple[SubChunkWithIndex | None, bool]:
    """from_sub_chunk_disk_payload decode a Disk encoding sub chunk and return its python represent.

    Args:
        r (Range): The whole chunk range where this sub chunk is in.
                   For overworld, it is Range(-64, 319).
        payload (bytes): The bytes of this sub chunk, who with a Disk encoding.

    Returns:
        tuple[SubChunkWithIndex | None, bool]: If failed to decode, then return (None, False).
                                               Otherwise, return decoded sub chunk and True.
    """
    index, sub_chunk_id, success = fscdp(r.start_range, r.end_range, payload)
    if not success:
        return (None, False)
    s = SubChunk()
    s._sub_chunk_id = sub_chunk_id
    return (SubChunkWithIndex(index, s), True)
