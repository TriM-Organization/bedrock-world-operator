from .types import LIB
from .types import CSlice, CString, CInt
from .types import as_c_bytes, as_python_bytes, as_python_string


LIB.DB_Has.argtypes = [CInt, CSlice]
LIB.DB_Get.argtypes = [CInt, CSlice]
LIB.DB_Put.argtypes = [CInt, CSlice, CSlice]
LIB.DB_Delete.argtypes = [CInt, CSlice]

LIB.DB_Has.restype = CInt
LIB.DB_Get.restype = CSlice
LIB.DB_Put.restype = CString
LIB.DB_Delete.restype = CString


def db_has(world_id: int, key: bytes) -> int:
    return int(LIB.DB_Has(CInt(world_id), as_c_bytes(key)))


def db_get(world_id: int, key: bytes) -> bytes:
    return as_python_bytes(LIB.DB_Get(CInt(world_id), as_c_bytes(key)))


def db_put(world_id: int, key: bytes, value: bytes) -> str:
    return as_python_string(
        LIB.DB_Put(CInt(world_id), as_c_bytes(key), as_c_bytes(value))
    )


def db_delete(world_id: int, key: bytes) -> str:
    return as_python_string(LIB.DB_Delete(CInt(world_id), as_c_bytes(key)))
