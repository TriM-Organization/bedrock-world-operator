import nbtlib
from .constant import DIMENSION_OVERWORLD
from ..world.chunk import Chunk
from ..world.sub_chunk import SubChunk
from ..internal.symbol_export_world import (
    load_biomes,
    load_chunk,
    load_chunk_payload_only,
    load_delta_update,
    load_delta_update_time_stamp,
    load_full_sub_chunk_blob_hash,
    load_nbt,
    load_nbt_payload_only,
    load_sub_chunk,
    load_sub_chunk_blob_hash,
    load_time_stamp,
    new_bedrock_world as nbw,
    release_bedrock_world,
    save_biomes,
    save_chunk,
    save_chunk_payload_only,
    save_delta_update,
    save_delta_update_time_stamp,
    save_full_sub_chunk_blob_hash,
    save_nbt,
    save_nbt_payload_only,
    save_sub_chunk,
    save_sub_chunk_blob_hash,
    save_time_stamp,
    world_close_world,
    world_get_level_dat,
    world_modify_level_dat,
)
from ..internal.symbol_export_world_underlying import (
    db_delete,
    db_get,
    db_has,
    db_put,
)
from ..world.define import ChunkPos, Dimension, HashWithPosY, SubChunkPos
from ..world.level_dat import LevelDat


class WorldBase:
    """WorldBase is the base implement of a Minecraft world game saves."""

    _world_id: int

    def __init__(self):
        self._world_id = -1

    def __del__(self):
        if self._world_id >= 0 and not release_bedrock_world is None:
            release_bedrock_world(self._world_id)

    def is_valid(self) -> bool:
        """
        is_valid check the opened world is valid or not.
        If not valid, it means current world is actually not opened.
        Try to use a world that not opened is not allowed, and any operation will be terminated.

        Returns:
            bool: The current world is valid or not.
        """
        return self._world_id >= 0

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
        ldt = LevelDat()

        result, success = world_get_level_dat(self._world_id)
        if not success:
            return None

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

    def load_biomes(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> bytes:
        """load_biomes loads the biome data of a chunk whose in chunk_pos and dm.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            bytes: The biome data of target chunk.
                   If meet error or not exist, then return empty bytes.
        """
        return load_biomes(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def save_biomes(
        self,
        chunk_pos: ChunkPos,
        biomes_data: bytes,
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """save_biomes set the biome data of a chunk whose in chunk_pos and dm.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            biomes_data (bytes): The biome data want to set to this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to set biome data.
        """
        err = save_biomes(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, biomes_data)
        if len(err) > 0:
            raise Exception(err)

    def load_chunk_payload_only(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> list[bytes]:
        """
        load_chunk_payload_only loads a chunk at the position passed from the leveldb database.
        Note that we here don't decode chunk data and just return the origin payload.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            list[bytes]: The raw payload of this chunk, where each element in the list corresponds to a sub block payload.
                         If meet error or not exist, then return empty list.
        """
        return load_chunk_payload_only(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def load_chunk(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> Chunk:
        """load_chunk loads a chunk at the position passed from the leveldb database.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            Chunk: If current world or the chunk is not exist, then return a invalid chunk, with a
                   invalid chunk range which is RANGE_INVALID.
                   Otherwise, if success, you will get a valid chunk.
                   Note that you could use c.is_valid() to check whether the chunk is valid or not.
        """
        c = Chunk()
        c._chunk_range.start_range, c._chunk_range.end_range, c._chunk_id = load_chunk(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z
        )
        return c

    def save_chunk_payload_only(
        self,
        chunk_pos: ChunkPos,
        payload: list[bytes],
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """
        save_chunk_payload_only saves multiple sub chunks payload to the leveldb database which all these sub chunks are in a chunk.
        Note that we also write the version of this chunk.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            payload (list[bytes]): The payload of each sub chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save payload chunk.
        """
        err = save_chunk_payload_only(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, payload
        )
        if len(err) > 0:
            raise Exception(err)

    def save_chunk(
        self,
        chunk_pos: ChunkPos,
        chunk: Chunk,
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """
        save_chunk saves a chunk at the position passed to the leveldb database.
        Note that we also write the version of this chunk.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            chunk (Chunk): The chunk we want to save to the game saves.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save chunk.
        """
        err = save_chunk(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, chunk._chunk_id
        )
        if len(err) > 0:
            raise Exception(err)

    def load_sub_chunk(
        self,
        sub_chunk_pos: SubChunkPos,
        dm: Dimension = DIMENSION_OVERWORLD,
    ) -> SubChunk:
        """load_sub_chunk loads a sub chunk at the position from the leveldb database.

        Args:
            sub_chunk_pos (SubChunkPos): The sub chunk pos of this sub chunk.
            dm (Dimension, optional): The dimension of this sub chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            SubChunk: If current world or the sub chunk is not exist, then return a invalid sub chunk.
                      Otherwise, return the target sub chunk.
                      Note that you could use s.is_valid() to check whether the sub chunk is valid or not.
        """
        s = SubChunk()
        s._sub_chunk_id = load_sub_chunk(
            self._world_id, dm.dm, sub_chunk_pos.x, sub_chunk_pos.y, sub_chunk_pos.z
        )
        return s

    def save_sub_chunk(
        self,
        sub_chunk_pos: SubChunkPos,
        sub_chunk: SubChunk,
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """
        save_sub_chunk saves a sub chunk at the position passed to the leveldb database.
        Note that we also write the version of the whole chunk where this sub chunk is in.

        Args:
            sub_chunk_pos (SubChunkPos): The sub chunk pos of this sub chunk.
            sub_chunk (SubChunk): The sub chunk we want to save to the game saves.
            dm (Dimension, optional): The dimension of this sub chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save sub chunk.
        """
        err = save_sub_chunk(
            self._world_id,
            dm.dm,
            sub_chunk_pos.x,
            sub_chunk_pos.y,
            sub_chunk_pos.z,
            sub_chunk._sub_chunk_id,
        )
        if len(err) > 0:
            raise Exception(err)

    def load_nbt_payload_only(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> bytes:
        """
        load_nbt_payload_only loads payload of all block entities from the chunk position passed.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            bytes: The raw NBT payload of all block entities in this chunk.
                   If meet error or not exist, then return empty bytes.
        """
        return load_nbt_payload_only(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def load_nbt(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> list[nbtlib.tag.Compound]:
        """load_nbt loads all block entities from the chunk position passed.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            list[nbtlib.tag.Compound]: The decoded block entities NBT of this chunk.
                                       If meet error or not exist, then return empty list.
        """
        return load_nbt(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def save_nbt_payload_only(
        self, chunk_pos: ChunkPos, payload: bytes, dm: Dimension = DIMENSION_OVERWORLD
    ):
        """save_nbt_payload_only saves a serialized NBT data to the chunk position passed.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            payload (bytes): The raw payload of all block entities NBT in this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save payload NBT
        """
        err = save_nbt_payload_only(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, payload
        )
        if len(err) > 0:
            raise Exception(err)

    def save_nbt(
        self,
        chunk_pos: ChunkPos,
        nbts: list[nbtlib.tag.Compound],
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """save_nbt saves all block NBT data to the chunk position passed.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            nbts (list[nbtlib.tag.Compound]): A list holds all block entities NBT data of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save NBT
        """
        err = save_nbt(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, nbts)
        if len(err) > 0:
            raise Exception(err)

    def load_delta_update(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> bytes:
        """
        load_delta_update load a custom purpose payload which related a chunk from leveldb database.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            bytes: The delta update payload of this chunk.
                   If meet error or not exist, then return empty bytes.
        """
        return load_delta_update(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def save_delta_update(
        self, chunk_pos: ChunkPos, payload: bytes, dm: Dimension = DIMENSION_OVERWORLD
    ):
        """
        save_delta_update save a custom purpose payload which related a chunk to leveldb database.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            dm (Dimension): The dimension of this chunk.
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            payload (bytes): The delta update payload want to set for this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save delta update payload.
        """
        err = save_delta_update(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, payload
        )
        if len(err) > 0:
            raise Exception(err)

    def load_time_stamp(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> int:
        """
        load_time_stamp load the last update unix time of a chunk whose in chunk_pos and dm.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            int: The last update unix time of this chunk.
                 Return -1 for current world is not exist,
                 Return 0 for the time stamp is not exist.
        """
        return load_time_stamp(self._world_id, dm.dm, chunk_pos.x, chunk_pos.z)

    def save_time_stamp(
        self, chunk_pos: ChunkPos, time_stamp: int, dm: Dimension = DIMENSION_OVERWORLD
    ):
        """
        save_time_stamp save the last update unix time of a chunk whose in chunk_pos and dm.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            time_stamp (int): The last update unix time that want to set for this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save time stamp.
        """
        err = save_time_stamp(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, time_stamp
        )
        if len(err) > 0:
            raise Exception(err)

    def load_delta_time_stamp(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> int:
        """
        load_delta_time_stamp load the last update unix time of a delta update
        which related to a chunk in chunk_pos and dm.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of the chunk.
            dm (Dimension, optional): The dimension of the chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            int: The last update unix time of the delta update.
                 Return -1 for current world is not exist,
                 Return 0 for the time stamp is not exist.
        """
        return load_delta_update_time_stamp(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z
        )

    def save_delta_time_stamp(
        self, chunk_pos: ChunkPos, time_stamp: int, dm: Dimension = DIMENSION_OVERWORLD
    ):
        """
        save_time_stamp save the last update unix time of a delta update which related to chunk in chunk_pos and dm.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of the chunk.
            time_stamp (int): The last update unix time that want to set for the delta update.
            dm (Dimension, optional): The dimension of the chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save time stamp.
        """
        err = save_delta_update_time_stamp(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z, time_stamp
        )
        if len(err) > 0:
            raise Exception(err)

    def load_full_sub_chunk_blob_hash(
        self, chunk_pos: ChunkPos, dm: Dimension = DIMENSION_OVERWORLD
    ) -> list[HashWithPosY]:
        """
        load_full_sub_chunk_blob_hash loads the blob hash of a chunk.
        Actually speaking, this is hash for multiple sub chunks
        (each sub chunks who have payload will have a hash value), not just a completely chunk.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            list[HashWithPosY]: The hashes of this chunk.
                                If not exist or meet error, then return empty list.
        """
        hashes = load_full_sub_chunk_blob_hash(
            self._world_id, dm.dm, chunk_pos.x, chunk_pos.z
        )
        result = []
        for i in hashes:
            result.append(HashWithPosY(i[1], i[0]))
        return result

    def save_full_sub_chunk_blob_hash(
        self,
        chunk_pos: ChunkPos,
        new_hash: list[HashWithPosY],
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """
        save_full_sub_chunk_blob_hash update the blob hash of a chunk.
        It's necessary to say that this is not a hash of a completely chunk,
        but are multiple hash for each sub chunk who have payload in this chunk.
        Note that:
            - If len(new_hash) is 0, then the blob hash
              data of this chunk will be delete.
            - Zero hash is allowed.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            chunk_pos (ChunkPos): The chunk pos of this chunk.
            hashes (list[HashWithPosY]): The hashes want to save to this chunk.
            dm (Dimension, optional): The dimension of this chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save blob hash of this chunk.
        """
        err = save_full_sub_chunk_blob_hash(
            self._world_id,
            dm.dm,
            chunk_pos.x,
            chunk_pos.z,
            [(i.PosY, i.Hash) for i in new_hash],
        )
        if len(err) > 0:
            raise Exception(err)

    def load_sub_chunk_blob_hash(
        self,
        sub_chunk_pos: SubChunkPos,
        dm: Dimension = DIMENSION_OVERWORLD,
    ) -> int:
        """
        load_sub_chunk_blob_hash loads the blob hash of a sub chunk that in sub_chunk_pos and in dm dimension.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            sub_chunk_pos (SubChunkPos): The sub chunk pos of this sub chunk.
            dm (Dimension, optional): The dimension of this sub chunk. Defaults to DIMENSION_OVERWORLD.

        Returns:
            int: The blob hash value of target sub chunk.
                 If meet error or not exist, then return -1.
                 Return 0 for a sub chunk that full of air.
        """
        return load_sub_chunk_blob_hash(
            self._world_id, dm.dm, sub_chunk_pos.x, sub_chunk_pos.y, sub_chunk_pos.z
        )

    def save_sub_chunk_blob_hash(
        self,
        sub_chunk_pos: SubChunkPos,
        hash: int,
        dm: Dimension = DIMENSION_OVERWORLD,
    ):
        """
        save_sub_chunk_blob_hash save the hash for sub chunk which in sub_chunk_pos and in dm dimension.
        Note that zero hash is allowed.
        This is not used by standard Minecraft, and just for some own purpose.

        Args:
            sub_chunk_pos (SubChunkPos): The sub chunk pos of this sub chunk.
            dm (Dimension, optional): The dimension of this sub chunk. Defaults to DIMENSION_OVERWORLD.

        Raises:
            Exception: When failed to save blob hash of this sub chunk.
        """
        err = save_sub_chunk_blob_hash(
            self._world_id,
            dm.dm,
            sub_chunk_pos.x,
            sub_chunk_pos.y,
            sub_chunk_pos.z,
            hash,
        )
        if len(err) > 0:
            raise Exception(err)


def new_world(dir: str) -> World:
    """
    new_world creates a new provider reading and writing from/to files under the path
    passed using default options. If a world is present at the path, new_world will
    parse its data and initialise the world with it.

    Args:
        dir (str): The minecraft bedrock leveldb path (folder path)

    Returns:
        World: If database can't be initialise or the level dat is cannot be
               parsed, then return a invalid world.
               Otherwise, the bedrock world will be created or opened, and we return the world.
               Note that you could use w.is_valid() to check the world is valid or not.
    """
    w = World()
    w._world_id = nbw(dir)
    return w
