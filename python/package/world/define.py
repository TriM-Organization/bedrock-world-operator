import nbtlib
from dataclasses import dataclass, field


@dataclass
class ChunkPos:
    """
    ChunkPos holds the position of a chunk. The type is provided as a utility struct for keeping track of a
    chunk's position. Chunks do not themselves keep track of that. Chunk positions are different from block
    positions in the way that increasing the X/Z by one means increasing the absolute value on the X/Z axis in
    terms of blocks by 16.
    """

    x: int = 0
    z: int = 0


@dataclass
class SubChunkPos:
    """
    SubChunkPos holds the position of a sub-chunk. The type is provided as a utility struct for keeping track of a
    sub-chunk's position. Sub-chunks do not themselves keep track of that. Sub-chunk positions are different from
    block positions in the way that increasing the X/Y/Z by one means increasing the absolute value on the X/Y/Z axis in
    terms of blocks by 16.
    """

    x: int = 0
    y: int = 0
    z: int = 0


@dataclass
class Range:
    """
    Range represents the height range of a Dimension in blocks. The first value
    of the Range holds the minimum Y value, the second value holds the maximum Y
    value.
    """

    start_range: int = 0
    end_range: int = 0


class Dimension:
    """
    Dimension is a dimension of a World. It influences a variety of
    properties of a World such as the building range, the sky colour and the
    behaviour of liquid blocks.
    """

    dm: int = 0

    def __init__(self, dm: int):
        """Init a new dimension represent.

        Args:
            dm (int): The id of this dimension.
        """
        self.dm = dm

    def range(self) -> Range:
        """range return the range that player could build block in this dimension.

        Returns:
            Range: The range that player could build block in this dimension.
                   If this dimension is not standard dimension, then redirect
                   to overworld range.
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
        For example, the height of overworld is 384
        due to "384 = 319 - (-64) + 1", and 319 is
        the max Y that overworld could build, and -64
        is the min Y that overworld could build.

        Returns:
            int: The height of this dimension.
                 If this dimension is not standard dimension, then redirect
                 to overworld height.
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


@dataclass
class HashWithPosY:
    Hash: int = 0
    PosY: int = 0
