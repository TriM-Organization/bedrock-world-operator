import ctypes, struct

LIB = ctypes.cdll.LoadLibrary("python/out.dll")

CPtr = ctypes.c_void_p
CSlice = CPtr
CString = ctypes.c_char_p
CInt = ctypes.c_int
CLongLong = ctypes.c_longlong


def as_c_bytes(b: bytes) -> ctypes.c_char_p:
    return ctypes.c_char_p(struct.pack("<I", len(b)) + b)


def as_python_bytes(slice: CSlice) -> bytes:
    l = struct.unpack("<I", ctypes.string_at(slice, 4))[0]
    return ctypes.string_at(slice, 4 + l)[4:]


def as_c_string(string: str) -> CString:
    return CString(bytes(string, encoding="utf-8"))


def as_python_string(c_string: bytes) -> str:
    if c_string is None:
        return ""
    return c_string.decode(encoding="utf-8")
