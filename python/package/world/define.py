import nbtlib, numpy
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChunkPos:
    """
    ChunkPos holds the position of a chunk. The type is provided as a utility struct for keeping track of a
    chunk's position.

    Chunks do not themselves keep track of that. Chunk positions are different from block positions in the
    way that increasing the X/Z by one means increasing the absolute value on the X/Z axis in terms of blocks
    by 16.

    Note that ChunkPos is a hashable and cannot be further modified object.
    """

    x: int = 0
    z: int = 0


@dataclass(frozen=True)
class SubChunkPos:
    """
    SubChunkPos holds the position of a sub-chunk. The type is provided as a utility struct for keeping
    track of a sub-chunk's position.

    Sub-chunks do not themselves keep track of that. Sub-chunk positions are different from block positions
    in the way that increasing the X/Y/Z by one means increasing the absolute value on the X/Y/Z axis in
    terms of blocks by 16.

    Note that SubChunkPos is a hashable and cannot be further modified object.
    """

    x: int = 0
    y: int = 0
    z: int = 0


@dataclass(frozen=True)
class Range:
    """
    Range represents the height range of a Dimension in blocks.

    The first value of the Range holds the minimum Y value,
    the second value holds the maximum Y value.

    Note that Range is a hashable and cannot be further modified object.
    """

    start_range: int = 0
    end_range: int = 0


@dataclass(frozen=True)
class Dimension:
    """
    Dimension is a dimension of a World.

    It influences a variety of properties of a World such as the building range,
    the sky color and the behavior of liquid blocks.

    Note that Dimension is a hashable and cannot be further modified object.

    Args:
        dm (int): The id of this dimension.
    """

    dm: int = 0

    def __int__(self) -> int:
        return self.dm

    def range(self) -> Range:
        """range returns the range that player could build block in this dimension.

        Returns:
            Range: The range that player could build block in this dimension.
                   If this dimension is not standard dimension, then redirect
                   to Overworld range.
        """
        match self.dm:
            case 0:
                return Range(-64, 319)
            case 1:
                return Range(0, 127)
            case 2:
                return Range(0, 255)
            case _:
                return Range(-64, 319)

    def height(self) -> int:
        """
        height returns the height of this dimension.

        For example, the height of Overworld is 384
        due to "384 = 319 - (-64) + 1", and 319 is
        the max Y that Overworld could build, and -64
        is the min Y that Overworld could build.

        Returns:
            int: The height of this dimension.
                 If this dimension is not standard dimension, then redirect
                 to Overworld height.
        """
        match self.dm:
            case 0:
                return 384
            case 1:
                return 128
            case 2:
                return 256
            case _:
                return 384

    def __str__(self) -> str:
        match self.dm:
            case 0:
                return "Overworld"
            case 1:
                return "Nether"
            case 2:
                return "End"
            case _:
                return f"Custom (id={self.dm})"


@dataclass
class BlockStates:
    """BlockState holds a combination of a name and properties."""

    Name: str = ""
    States: nbtlib.tag.Compound = field(default_factory=lambda: nbtlib.tag.Compound())


# ptr = ((y >> 4) - (self.start_range >> 4)) << 12
# offset = x * 256 + (y & 15) * 16 + z
@dataclass
class QuickChunkBlocks:
    """
    QuickChunkBlocks is a quick blocks getter and setter,
    which used for a Minecraft chunk.

    Note that it is only representing the blocks in one
    layer in this chunk.

    Actually, the chunk biomes data is also similar to this
    data struct, so QuickChunkBlocks can also representing
    the biome IDs for each block in this chunk.

    Args:
        blocks (list[int], optional): A dense matrix that represents each block in a layer of this chunk.
                                      If this is used for biome data, then this matrix represents the
                                      biome ID for each blocks in this chunk.
                                      Default to an empty list.
        start_range (int): The min Y position of this chunk.
                           For Overworld is -64, but Nether and End is 0.
                           Default to -64.
        end_range (int): The max Y position of this chunk.
                         For Overworld is 319, for Nether is 127, and for End is 255.
                         Defaults to 319.
    """

    blocks: numpy.ndarray = field(default_factory=lambda: numpy.array([], dtype="<u4"))
    start_range: int = -64
    end_range: int = 319

    def set_empty(self, default_id: int):
        """
        set_empty make this chunk full of one thing.

        If QuickChunkBlocks is used to represent blocks,
        then set_empty make this chunk full of air.

        Otherwise, this QuickChunkBlocks is represents to the
        biome ID of each block, and set_empty will make the
        biome ID of each block in this chunk as default_id.

        Args:
            default_id (int): The block runtime ID of air block or the default biome id.
        """
        self.blocks = numpy.full(
            4096 * ((self.end_range - self.start_range + 1) >> 4),
            default_id,
            dtype="<u4",
        )

    def block(self, x: int, y: int, z: int) -> numpy.uint32:
        """
        block returns the runtime ID of the block at a given x, y and z in this chunk.

        If QuickChunkBlocks is used to represents the biome data of this chunk,
        then block return the biome ID of the block at (x,y,z).

        Note that this function will not check whether the index is overflowing.

        Args:
            x (int): The relative x position of this block. Must in a range of 0-15.
            y (int): The y position of this block.
                     Must in a range of -64~319 (Overworld), 0-127 (Nether) and 0-255 (End).
            z (int): The relative z position of this block. Must in a range of 0-15.

        Returns:
            int: Return the block runtime ID of target block.
                 Or, if QuickChunkBlocks is used to represents the biome data of this chunk,
                 then return the biome ID of target block.
        """
        return self.blocks[
            (((y >> 4) - (self.start_range >> 4)) << 12) + x * 256 + (y & 15) * 16 + z
        ]

    def set_block(self, x: int, y: int, z: int, id: int | numpy.uint32):
        """
        set_block sets the runtime ID of a block at a given x, y and z in this chunk.

        If QuickChunkBlocks is used to represents the biome data of this chunk,
        then set_block sets the biome ID of the block at (x,y,z).

        Note that:
            - This operation is just on program, and you need to use c.set_blocks(layer, QuickChunkBlocks) to apply
              changes to the chunk. Then, after you apply changes, use w.save_chunk(...) to apply changes to the game saves.
            - It will not check whether the index is overflowing.

        Args:
            x (int): The relative x position of this block. Must in a range of 0-15.
            y (int): The y position of this block.
                     Must in a range of -64~319 (Overworld), 0-127 (Nether) and 0-255 (End).
            z (int): The relative z position of this block. Must in a range of 0-15.
            id (int | numpy.uint32): The runtime ID of result block that this block will be.
                      Or, if QuickChunkBlocks is used to represents the biome data of this chunk,
                      then id is the biome id of this block that you want to set.
        """
        self.blocks[
            (((y >> 4) - (self.start_range >> 4)) << 12) + x * 256 + (y & 15) * 16 + z
        ] = id


@dataclass
class QuickSubChunkBlocks:
    """
    QuickSubChunkBlocks is a quick blocks getter and setter,
    which used for a Minecraft sub chunk.

    Note that it is only representing one layer in this sub chunk.

    Args:
        blocks (list[int], optional): A dense matrix that represents each block in a layer of this sub chunk.
                                      Default to an empty list.
    """

    blocks: numpy.ndarray = field(default_factory=lambda: numpy.array([], dtype="<u4"))

    def set_empty(self, air_block_runtime_id: int):
        """set_empty make this sub chunk full of air.

        Args:
            air_block_runtime_id (int): The block runtime ID of air block.
        """
        self.blocks = numpy.full(4096, air_block_runtime_id, dtype="<u4")

    def block(self, x: int, y: int, z: int) -> numpy.uint32:
        """
        block returns the runtime ID of the block
        located at the given X, Y and Z.

        X, Y and Z must be in a range of 0-15.

        Args:
            x (int): The relative x position of target block. Must in a range of 0-15.
            y (int): The relative y position of target block. Must in a range of 0-15.
            z (int): The relative z position of target block. Must in a range of 0-15.

        Returns:
            int: Return the block runtime ID of target block.
                 It will not check whether the index is overflowing.
        """
        return self.blocks[x * 256 + y * 16 + z]

    def set_block(self, x: int, y: int, z: int, block_runtime_id: int | numpy.uint32):
        """
        set_block sets the given block runtime
        ID at the given X, Y and Z.

        X, Y and Z must be in a range of 0-15.

        Note that:
            - This operation is just on program, and you need to use s.set_blocks(layer, QuickSubChunkBlocks) to apply changes
              to the sub chunk. Then, after you apply changes,
                - use w.save_sub_chunk(...) to apply changes to the game saves.
                - if this sub chunk is from a loaded chunk, then you'd be suggested to use w.save_chunk(...) to apply changes
                  to the game saves if there are multiple sub chunk changes in the target chunk.
            - It will not check whether the index is overflowing.

        Args:
            x (int): The relative x position of target block. Must in a range of 0-15.
            y (int): The relative y position of target block. Must in a range of 0-15.
            z (int): The relative z position of target block. Must in a range of 0-15.
            block_runtime_id (int | numpy.uint32): The block runtime ID of target block will be.
        """
        self.blocks[x * 256 + y * 16 + z] = block_runtime_id


@dataclass(frozen=True)
class HashWithPosY:
    """Note that HashWithPosY is a hashable and cannot be further modified object."""

    Hash: int = 0
    PosY: int = 0
