import nbtlib
from python.internal.symbol_export_world import (
    load_biomes,
    load_chunk_payload_only,
    release_bedrock_world,
    save_biomes,
    world_close_world,
    world_get_level_dat,
    world_modify_level_dat,
)
from python.internal.symbol_export_world_underlying import (
    db_delete,
    db_get,
    db_has,
    db_put,
)
from python.world.define import ChunkPos, Dimension
from python.world.level_dat import LevelDat


class WorldBase:
    """WorldBase is the base implement of a Minecraft world game saves."""

    _world_id: int

    def __init__(self):
        self._world_id = -1

    def __del__(self):
        if self._world_id >= 0:
            release_bedrock_world(self._world_id)

    def close_world(self):
        """close_world close this game saves.

        Raises:
            Exception: When failed to close the world.
        """
        err = world_close_world(self._world_id)
        if len(err) > 0:
            raise Exception(err)

    def has(self, key: bytes) -> bool:
        """has check the if the key is in the underlying database of this game saves.

        Args:
            key (bytes): The bytes represent of the key.

        Returns:
            bool: If key is exist, then this is true.
                  Otherwise, when meet error or not exist, return false.
        """
        return db_has(self._world_id, key) == 1

    def get(self, key: bytes) -> bytes:
        """get try to get the value of the key in the underlying database.

        Args:
            key (bytes): The bytes represent of the key.

        Returns:
            bytes: If key is exist, then return the value of this key.
                   Otherwise, when meet error or not exist, return empty bytes.
        """
        return db_get(self._world_id, key)

    def put(self, key: bytes, value: bytes):
        """put set the key to value in the underlying database.

        Args:
            key (bytes): The bytes represent of the key.
            value (bytes): The bytes represent of the value.

        Raises:
            Exception: When failed to set the value of this key.
        """
        err = db_put(self._world_id, key, value)
        if len(err) > 0:
            raise Exception(err)

    def delete(self, key: bytes):
        """delete remove the key and its value from the underlying database.

        Args:
            key (bytes): The bytes represent of the key.

        Raises:
            Exception: When failed to remove the key from the database.
        """
        err = db_delete(self._world_id, key)
        if len(err) > 0:
            raise Exception(err)


class World(WorldBase):
    """
    World is the completely implements of Minecraft bedrock game saves,
    which only entities and player data related things are not implement.
    """

    def __init__(self):
        super().__init__()

    def get_level_dat(self) -> LevelDat | None:
        """get_level_dat get the level dat of current game saves.

        Returns:
            LevelDat | None:
                If success, then return the level dat.
                Otherwise, return None.
        """
        result, success = world_get_level_dat(self._world_id)
        if not success:
            return None
        ldt = LevelDat()
        ldt.unmarshal(result)  # type: ignore
        return ldt

    def modify_level_dat(self, new_level_dat: LevelDat):
        """modify_level_dat set the level dat of this world to new_level_dat.

        Args:
            new_level_dat (LevelDat): The new level dat want to set.

        Raises:
            Exception: When failed to set level dat.
        """
        err = world_modify_level_dat(self._world_id, new_level_dat.marshal())
        if len(err) > 0:
            raise Exception(err)

    def load_biomes(self, dm: Dimension, chunk_pos: ChunkPos) -> bytes:
        """load_biomes loads the biome data of a chunk whose in chunk_pos and dm.

        Args:
            dm (Dimension): The dimension of this chunk.
            chunk_pos (ChunkPos): The chunk pos of this chunk.

        Returns:
            bytes: The biome data of target chunk.
                   If meet error or not exist, then return empty bytes.
        """
        return load_biomes(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def save_biomes(self, dm: Dimension, chunk_pos: ChunkPos, biomes_data: bytes):
        """save_biomes set the biome data of a chunk whose in chunk_pos and dm.

        Args:
            dm (Dimension): The dimension of this chunk.
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            biomes_data (bytes): The biome data want to set to this chunk.

        Raises:
            Exception: When failed to set biome data.
        """
        err = save_biomes(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, biomes_data)
        if len(err) > 0:
            raise Exception(err)

    def load_chunk_payload_only(
        self, dm: Dimension, chunk_pos: ChunkPos
    ) -> list[bytes]:
        """
        load_chunk_payload_only loads a chunk at the position passed from the leveldb database.
        Note that we here don't decode chunk data and just return the origin payload.

        Args:
            dm (Dimension): The dimension of this chunk.
            chunk_pos (ChunkPos): The chunk pos of this chunk.

        Returns:
            list[bytes]: The raw payload of this chunk.
                         If meet error or not exist, then return empty list.
        """
        return load_chunk_payload_only(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)
