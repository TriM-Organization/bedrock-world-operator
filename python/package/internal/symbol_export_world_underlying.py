from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_python_string


LIB.DB_Has.argtypes = [CLongLong, CSlice]
LIB.DB_Get.argtypes = [CLongLong, CSlice]
LIB.DB_Put.argtypes = [CLongLong, CSlice, CSlice]
LIB.DB_Delete.argtypes = [CLongLong, CSlice]

LIB.DB_Has.restype = CInt
LIB.DB_Get.restype = CSlice
LIB.DB_Put.restype = CString
LIB.DB_Delete.restype = CString


def db_has(world_id: int, key: bytes) -> int:
    return int(LIB.DB_Has(CLongLong(world_id), as_c_bytes(key)))


def db_get(world_id: int, key: bytes) -> bytes:
    return as_python_bytes(LIB.DB_Get(CLongLong(world_id), as_c_bytes(key)))


def db_put(world_id: int, key: bytes, value: bytes) -> str:
    return as_python_string(
        LIB.DB_Put(CLongLong(world_id), as_c_bytes(key), as_c_bytes(value))
    )


def db_delete(world_id: int, key: bytes) -> str:
    return as_python_string(LIB.DB_Delete(CLongLong(world_id), as_c_bytes(key)))
