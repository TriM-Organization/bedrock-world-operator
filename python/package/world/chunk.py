from ..internal.symbol_export_chunk import (
    chunk_biome,
    chunk_block,
    chunk_compact,
    chunk_equals,
    chunk_highest_filled_sub_chunk,
    chunk_range,
    chunk_set_biome,
    chunk_set_block,
    chunk_sub,
    chunk_sub_chunk,
    chunk_sub_index,
    chunk_sub_y,
    new_chunk as nc,
    release_chunk,
)
from ..world.define import Range
from ..world.sub_chunk import SubChunk


class ChunkBase:
    """ChunkBase is the base implement of a Minecraft chunk."""

    _chunk_id: int

    def __init__(self):
        self._chunk_id = -1

    def __del__(self):
        if self._chunk_id >= 0 and not release_chunk is None:
            release_chunk(self._chunk_id)


class Chunk(ChunkBase):
    """
    Chunk is a segment in the world with a size of 16x16x256 blocks. A chunk contains multiple sub chunks
    and stores other information such as biomes.
    It is not safe to call methods on Chunk simultaneously from multiple goroutines.
    """

    def __init__(self):
        super().__init__()

    def biome(self, x: int, y: int, z: int) -> int:
        """biome returns the biome ID at a specific column in the chunk.

        Args:
            x (int): The relative x position of this column. Must in a range of 0-15.
            y (int): The relative y position of this column.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).
            z (int): The relative z position of this column. Must in a range of 0-15.

        Returns:
            int: The biome ID of this column.
                 If current chunk is not found, then return -1.
        """
        return chunk_biome(self._chunk_id, x, y, z)

    def block(self, x: int, y: int, z: int, layer: int) -> int:
        """Block returns the runtime ID of the block at a given x, y and z in a chunk at the given layer.

        Args:
            x (int): The relative x position of this block. Must in a range of 0-15.
            y (int): The relative y position of this block.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).
            z (int): The relative z position of this block. Must in a range of 0-15.
            layer (int): The layer to find this block.

        Returns:
            int: Return the block runtime ID of target block.
                 If current chunk is not found, then return -1.
                 Note that if no sub chunk exists at the given y, the block is assumed to be air.
        """
        return chunk_block(self._chunk_id, x, y, z, layer)

    def compact(self):
        """
        compact compacts the chunk as much as possible, getting rid of any sub chunks that are empty,
        and compacts all storages in the sub chunks to occupy as little space as possible.
        compact should be called right before the chunk is saved in order to optimise the storage space.

        Raises:
            Exception: When failed to compact.
        """
        err = chunk_compact(self._chunk_id)
        if len(err) > 0:
            raise Exception(err)

    def equals(self, another_chunk: ChunkBase) -> tuple[bool, bool]:
        """equals returns if the chunk passed is equal to the current one.

        Args:
            another_chunk (ChunkBase): The chunk passed.

        Returns:
            tuple[bool, bool]: The first element refer to the compare result,
                               and the second one refer to if their have any
                               any error occurred.
                               If the second one is False, then it means current
                               chunk or another_chunk is not found.
        """
        result = chunk_equals(self._chunk_id, another_chunk._chunk_id)
        return (result == 1, result != -1)

    def highest_filled_sub_chunk(self) -> int:
        """
        highest_filled_sub_chunk returns the index of the highest sub chunk in the chunk
        that has any blocks in it. 0 is returned if no subchunks have any blocks.

        Returns:
            int: The index of the highest sub chunk in the chunk that has any blocks in it.
                 If no subchunks have any block, then return 0.
                 Additionally, if current chunk is not found, then return -1.
        """
        return chunk_highest_filled_sub_chunk(self._chunk_id)

    def range(self) -> tuple[Range, bool]:
        """Range returns the Range of the Chunk as passed to new_chunk.

        Returns:
            tuple[Range, bool]: If current chunk is not found, return (Range(0,0), False).
                                Otherwise, return the range and True.
        """
        start_range, end_range, ok = chunk_range(self._chunk_id)
        if not ok:
            return (Range(0, 0), False)
        return (Range(start_range, end_range), True)

    def set_biome(self, x: int, y: int, z: int, biome_id: int):
        """set_biome sets the biome ID at a specific column in the chunk.

        Args:
            x (int): The relative x position of this column. Must in a range of 0-15.
            y (int): The relative y position of this column.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).
            z (int): The relative z position of this column. Must in a range of 0-15.
            biome_id (int): The biome ID want to set.

        Raises:
            Exception: When failed to set biome ID.
        """
        err = chunk_set_biome(self._chunk_id, x, y, z, biome_id)
        if len(err) > 0:
            raise Exception(err)

    def set_block(self, x: int, y: int, z: int, layer: int, block_runtime_id: int):
        """
        set_block sets the runtime ID of a block at a given x, y and z in a chunk at the given layer.
        If no SubChunk exists at the given y, a new SubChunk is created and the block is set.

        Args:
            x (int): The relative x position of this block. Must in a range of 0-15.
            y (int): The relative y position of this block.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).
            z (int): The relative z position of this block. Must in a range of 0-15.
            layer (int): The layer that this block in.
            block_runtime_id (int): The result block that this block will be.

        Raises:
            Exception: When failed to set block.
        """
        err = chunk_set_block(self._chunk_id, x, y, z, layer, block_runtime_id)
        if len(err) > 0:
            raise Exception(err)

    def sub(self) -> list[SubChunk]:
        """sub returns a list of all sub chunks present in the chunk.

        Returns:
            list[SubChunk]: All sub chunks present in the chunk.
                            If current chunk is not found, or this chunk have no sub chunk, then return empty list.
        """
        result = []
        for i in chunk_sub(self._chunk_id):
            s = SubChunk()
            s._sub_chunk_id = i
            result.append(s)
        return result

    def sub_chunk(self, y: int) -> tuple[SubChunk | None, bool]:
        """sub_chunk finds the correct SubChunk in the Chunk by a Y value.

        Args:
            y (int): The relative y position of this block.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).

        Returns:
            tuple[SubChunk | None, bool]: If current chunk is not found, then return (None, False).
                                          Otherwise, return the target sub chunk and True.
                                          Note that if this sub chunk is not exist,
                                          the the program will crash (The try statement can't solve).
        """
        sub_chunk_id = chunk_sub_chunk(self._chunk_id, y)
        if sub_chunk_id == -1:
            return (None, False)
        s = SubChunk()
        s._sub_chunk_id = sub_chunk_id
        return (s, True)

    def sub_index(self, y: int) -> int:
        """sub_index returns the sub chunk Y index matching the y value passed.

        Args:
            y (int): The relative y position of this block.
                     Must in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).

        Returns:
            int: The y index.
                 If current sub chunk is not found, then return -1.
        """
        return chunk_sub_index(self._chunk_id, y)

    def sub_y(self, index: int) -> int:
        """sub_y returns the sub chunk Y value matching the index passed.

        Args:
            index (int): The given index that used to compute the value of Y.

        Returns:
            int: The Y value who could match the given index.
                 Y is in a range of -4~19 (Overworld), 0-7 (Nether) and 0-15 (End).
                 If current sub chunk is not found, then return -1.
        """
        return chunk_sub_y(self._chunk_id, index)


def new_chunk(r: Range) -> Chunk:
    """NewChunk initialises a new chunk who full of air and returns it, so that it may be used.

    Args:
        r (Range): The Y range of this chunk could reach.

    Returns:
        Chunk: A new chunk.
    """
    c = Chunk()
    c._chunk_id = nc(r.start_range, r.end_range)
    return c
