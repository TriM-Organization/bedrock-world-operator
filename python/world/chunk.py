from python.internal.symbol_export_chunk import chunk_biome, release_chunk


class Chunk:
    """
    Chunk is a segment in the world with a size of 16x16x256 blocks. A chunk contains multiple sub chunks
    and stores other information such as biomes.
    It is not safe to call methods on Chunk simultaneously from multiple goroutines.
    """

    _chunk_id: int

    def __init__(self):
        self._chunk_id = -1

    def __del__(self):
        if self._chunk_id >= 0:
            release_chunk(self._chunk_id)

    def biome(self, x: int, y: int, z: int) -> tuple[int, bool]:
        """biome returns the biome ID at a specific column in the chunk.

        Args:
            x (int): The x position of this column.
            y (int): The y position of this column.
            z (int): The z position of this column.

        Returns:
            tuple[int, bool]: Return (x, True) for find the biome id (x) of this column.
                              Return (0, False) for not found or meet error.
        """
        result = chunk_biome(self._chunk_id, x, y, z)
        if result == -1:
            return (0, False)
        return (result, True)
