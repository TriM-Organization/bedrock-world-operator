import nbtlib
import numpy
from dataclasses import dataclass
from .constant import (
    AIR_BLOCK_STATES,
    CURRENT_BLOCK_VERSION,
    EMPTY_BLOCK_STATES,
    INVALID_BLOCK_RUNTIME_ID,
)
from ..internal.symbol_export_block_table import (
    new_block_table as _new_block_table,
    release_block_table,
    table_air_runtime_id,
    table_finalise_register,
    table_register_custom_block,
    table_register_permutation,
    table_runtime_id_to_state,
    table_state_to_runtime_id,
    table_use_network_id_hashes,
)
from ..world.define import BlockStates, StateEnum


@dataclass
class BlockTableBase:
    """BlockTableBase is the base implement of a block runtime ID table."""

    _table_id: int = -1

    def __del__(self):
        if self._table_id >= 0 and release_block_table is not None:
            release_block_table(self._table_id)

    def is_valid(self) -> bool:
        """
        is_valid check current table is valid or not.

        If not valid, it means the table actually not exist,
        not only Python but also in Go.

        Try to use an invalid table is not allowed,
        and any operation will be terminated.

        Returns:
            bool: Whether the table is valid or not.
        """
        return self._table_id >= 0


class BlockTable(BlockTableBase):
    """
    BlockRuntimeIDTable is a block runtime ID table that
    supports converting blocks between blocks themselves
    and their runtime IDs description.
    """

    def __init__(self):
        super().__init__()

    def air_runtime_id(self) -> int:
        """air_runtime_id returns the runtime ID of the air block.

        Returns:
            int: The runtime ID of the air block.
                 If the current table is not found, then return -1.
        """
        return table_air_runtime_id(self._table_id)

    def use_network_id_hashes(self) -> bool:
        """
        use_network_id_hashes returns if the block
        runtime IDs are using network hashes or not.

        Returns:
            bool: Return True if the block runtime IDs are using network hashes.
                  Return False for not use hashes, or the current table is not found.
        """
        result = table_use_network_id_hashes(self._table_id)
        return result == 1

    def runtime_id_to_state(
        self,
        block_runtime_id: int | numpy.uint32,
    ) -> BlockStates:
        """runtime_id_to_state convert block runtime ID to a BlockStates.

        Args:
            block_runtime_id (int | numpy.uint32): The runtime ID of target block.

        Returns:
            BlockStates: If target block or current table is not found, return AIR_BLOCK_STATES.
                         Otherwise, return the founded block states.
        """
        block_states = BlockStates()

        name, states, success = table_runtime_id_to_state(
            self._table_id, block_runtime_id  # type: ignore
        )
        if not success:
            return AIR_BLOCK_STATES

        block_states.Name, block_states.States = name, states  # type: ignore
        return block_states

    def state_to_runtime_id(
        self, block_name: str, block_states: nbtlib.tag.Compound = EMPTY_BLOCK_STATES
    ) -> int | numpy.uint32:
        """
        state_to_runtime_id convert a block which name is block_name
        and states is block_states to its block runtime ID represent.

        Note that the internal implement will try to upgrade the block states
        to the newest version, and then do runtime id conversion.

        Therefore, it's safe to use a older version states to convert to block
        runtime id.

        Args:
            block_name (str): The name of this block.
            block_states (nbtlib.tag.Compound, optional): The block states of this block.
                                                          Defaults to EMPTY_BLOCK_STATES.

        Returns:
            int | numpy.uint32: If target block or current table is not found,
                                return INVALID_BLOCK_RUNTIME_ID.
                                Otherwise, return its block runtime ID.
        """
        block_runtime_id, success = table_state_to_runtime_id(
            self._table_id, block_name, block_states
        )
        if not success:
            return INVALID_BLOCK_RUNTIME_ID
        return block_runtime_id

    def register_custom_block(
        self,
        block_name: str,
        block_states: nbtlib.tag.Compound = EMPTY_BLOCK_STATES,
        block_version: int = CURRENT_BLOCK_VERSION,
    ):
        """
        register_custom_block register a custom block which name is block_name,
        states is block_states and version is block_version to current table.

        block_version is the version of blocks (states) of the game. This version
        is composed of 4 bytes indicating a version, interpreted as a big endian int.
        The current version represents 1.21.1.0 {1, 21, 1, 0} which is 18153728.

        Note that you MUST call FinaliseRegister atfer register all custom blocks.

        Args:
            block_name (str): The name of this block.
            block_states (nbtlib.tag.Compound, optional): The block states of this block.
                                                          Defaults to EMPTY_BLOCK_STATES.
            block_version (int, optional): The version of this block.
                                           Defaults to CURRENT_BLOCK_VERSION.

        Raises:
            Exception: When failed to register custom block.
        """
        err = table_register_custom_block(
            self._table_id, block_name, block_states, block_version
        )
        if len(err) > 0:
            raise Exception(err)

    def register_permutation(
        self,
        block_name: str,
        block_version: int = CURRENT_BLOCK_VERSION,
        states_enum: list[StateEnum] = [],
    ):
        """
        register_permutation registers all block states of a custom block to the table.

        block_version is the version of blocks (states) of the game. This version
        is composed of 4 bytes indicating a version, interpreted as a big endian int.
        The current version represents 1.21.1.0 {1, 21, 1, 0} which is 18153728.

        Note that you MUST call FinaliseRegister after register all custom blocks.

        Args:
            block_name (str): The name of this block.
            block_version (int, optional): The version of this block.
                                           Defaults to CURRENT_BLOCK_VERSION.
            states_enum (list[StateEnum], optional):
                A list of state enums that the block can have.
                Each element means a state key and its possible values.
                Defaults to [].

        Raises:
            Exception: When failed to register permutation.
        """
        err = table_register_permutation(
            self._table_id,
            block_name,
            block_version,
            [(i.state_key_name, i.possible_values) for i in states_enum],
        )
        if len(err) > 0:
            raise Exception(err)

    def finalise_register(self):
        """
        finalise_register is called after blocks have finished
        registering and the palette can be sorted and hashed.

        Raises:
            Exception: When failed to finalise register.
        """
        err = table_finalise_register(self._table_id)
        if len(err) > 0:
            raise Exception(err)


def new_block_table(use_network_id_hashes: bool = True) -> BlockTable:
    """new_block_table returns a new block runtime ID table.

    Args:
        use_network_id_hashes (bool, optional):
            Indicates whether the runtime IDs are the network ID hashes.
            Defaults to True.

    Returns:
        BlockTable: A block runtime ID table that supports converting blocks
                    between blocks themselves and their runtime IDs description.
    """
    t = BlockTable()
    t._table_id = _new_block_table(use_network_id_hashes)
    return t
