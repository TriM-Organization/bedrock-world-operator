import nbtlib
from ..internal.symbol_export_block_convert import (
    runtime_id_to_state as rits,
    state_to_runtime_id as stri,
)
from ..world.define import BlockStates


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
