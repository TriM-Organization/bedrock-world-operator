from dataclasses import dataclass, field
from .define import QuickSubChunkBlocks
from ..internal.symbol_export_sub_chunk import (
    new_sub_chunk as nsc,
    release_sub_chunk,
    sub_chunk_block,
    sub_chunk_blocks,
    sub_chunk_empty,
    sub_chunk_equals,
    sub_chunk_set_block,
    sub_chunk_set_blocks,
)


class SubChunkBase:
    """SubChunkBase is the base implement of a Minecraft sub chunk."""

    _sub_chunk_id: int

    def __init__(self):
        self._sub_chunk_id = -1

    def __del__(self):
        if self._sub_chunk_id >= 0 and not release_sub_chunk is None:
            release_sub_chunk(self._sub_chunk_id)

    def is_valid(self) -> bool:
        """
        is_valid check current sub chunk is valid or not.

        If not valid, it means the sub chunk actually not exist,
        not only Python but also in Go.

        Try to use an invalid sub chunk is not allowed,
        and any operation will be terminated.

        Returns:
            bool: Whether the sub chunk is valid or not.
        """
        return self._sub_chunk_id >= 0


class SubChunk(SubChunkBase):
    """
    SubChunk is a cube of blocks located in a chunk.

    It has a size of 16x16x16 blocks and forms part
    of a stack that forms a Chunk.
    """

    def __init__(self):
        super().__init__()

    def equals(self, another_sub_chunk: SubChunkBase) -> bool:
        """Equals returns if the sub chunk passed is equal to the current one.

        Args:
            another_sub_chunk (SubChunkBase): The sub chunk passed.

        Returns:
            bool: The compare result.
                  Return True for the contents of two sub chunks is the same.
                  Return False for the current sub chunk or another_sub_chunk is not found.
        """
        result = sub_chunk_equals(self._sub_chunk_id, another_sub_chunk._sub_chunk_id)
        return result == 1

    def empty(self) -> bool:
        """
        empty checks if the SubChunk is considered empty.

        This is the case if the SubChunk has 0 block storage
        or if it has a single one that is filled with air.

        Returns:
            bool: Return True for the sub chunk is empty.
                  Return False for the sub chunk is not empty, or the current sub chunk is not found.
        """
        result = sub_chunk_empty(self._sub_chunk_id)
        return result == 1

    def block(self, x: int, y: int, z: int, layer: int) -> int:
        """
        block returns the runtime ID of the block
        located at the given X, Y and Z.

        X, Y and Z must be in a range of 0-15.

        Args:
            x (int): The relative x position of target block. Must in a range of 0-15.
            y (int): The relative y position of target block. Must in a range of 0-15.
            z (int): The relative z position of target block. Must in a range of 0-15.
            layer (int): The layer that the target block is in.

        Returns:
            int: Return the block runtime ID of target block.
                 If the current sub chunk is not found, then return -1.
                 Note that if no sub chunk exists at the given y, the block is assumed to be air.
        """
        return sub_chunk_block(self._sub_chunk_id, x, y, z, layer)

    def blocks(self, layer: int) -> QuickSubChunkBlocks:
        """
        blocks all blocks (block runtime ids) whose in layer.

        It is highly suggested you use this instead of s.block(...)
        if you are trying to query so many blocks from this sub chunk.

        Args:
            layer (int): The sub chunk blocks you want to find.
                         layer refers to the found blocks from this layer.

        Returns:
            QuickSubChunkBlocks:
                All blocks of the target layer in this sub chunk if the current sub chunk exists.
                If the target layer does not exist, then you get a sub chunk full of air.
                Note that this implement doesn't do further check (maybe the underlying blocks list is empty)
                due to this is aims to increase block query/set speed, and you should take responsibility for
                any possible error.
        """
        return QuickSubChunkBlocks(sub_chunk_blocks(self._sub_chunk_id, layer))

    def set_block(self, x: int, y: int, z: int, layer: int, block_runtime_id: int):
        """
        set_block sets the given block runtime
        ID at the given X, Y and Z.

        X, Y and Z must be in a range of 0-15.

        Args:
            x (int): The relative x position of target block. Must in a range of 0-15.
            y (int): The relative y position of target block. Must in a range of 0-15.
            z (int): The relative z position of target block. Must in a range of 0-15.
            layer (int): The layer that the target block is in.
            block_runtime_id (int): The block runtime id of target block will be.

        Raises:
            Exception: When failed to set block.
        """
        err = sub_chunk_set_block(self._sub_chunk_id, x, y, z, layer, block_runtime_id)
        if len(err) > 0:
            raise Exception(err)

    def set_blocks(self, layer: int, blocks: QuickSubChunkBlocks):
        """
        set_blocks sets the whole chunk blocks in layer by given block runtime ids.

        It is highly suggested you use this instead of s.set_block(...) if you are
        trying to modify so many blocks to this sub chunk.

        Note that this implement will not check the underlying blocks list is valid
        or not due to this is aims to increase block query/set speed, and you should
        take responsibility for any possible error.

        Args:
            layer (int): The blocks in the target layer of this chunk that you want to overwrite.

        Raises:
            Exception: When failed to set blocks.
        """
        err = sub_chunk_set_blocks(self._sub_chunk_id, layer, blocks.blocks)
        if len(err) > 0:
            raise Exception(err)


@dataclass
class SubChunkWithIndex:
    """
    SubChunkWithIndex represents a sub chunk and its
    index in a whole chunk where this sub chunk is in.

    Args:
        sub_chunk (SubChunk): The sub chunk.
        index (int): The index of this sub chunk, and must be bigger than -1.
                     For example, for a block in (x, -63, z), then its
                     sub chunk Y pos will be -63>>4 (-4).
                     However, this is not the index of this sub chunk,
                     and we need to do other compute to get the index:
                     index = (-63>>4) - (r.start_range>>4)
                           = (-63>>4) - (-64>>4)
                           = 0
    """

    index: int = 0
    sub_chunk: SubChunk = field(default_factory=lambda: SubChunk())


def new_sub_chunk() -> SubChunk:
    """
    NewSubChunk creates a new sub chunk.

    All sub chunks should be created
    through this function.

    Returns:
        SubChunk: A new sub chunk that is full of air.
    """
    s = SubChunk()
    s._sub_chunk_id = nsc()
    return s
