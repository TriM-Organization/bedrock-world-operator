import struct, nbtlib
from io import BytesIO
from .types import LIB
from .types import CSlice, CString, CInt
from .types import as_c_bytes, as_python_bytes, as_c_string
from ..utils import marshalNBT, unmarshalNBT


LIB.RuntimeIDToState.argtypes = [CInt]
LIB.StateToRuntimeID.argtypes = [CString, CSlice]

LIB.RuntimeIDToState.restype = CSlice
LIB.StateToRuntimeID.restype = CSlice


def runtime_id_to_state(
    block_runtime_id: int,
) -> tuple[str, nbtlib.tag.Compound | None, bool]:
    payload = as_python_bytes(LIB.RuntimeIDToState(CInt(block_runtime_id)))
    reader = BytesIO(payload)

    if reader.read(1) == b"\x00":
        return ("", None, False)

    l: int = struct.unpack("<H", reader.read(2))[0]
    name = reader.read(l).decode(encoding="utf-8")

    l = struct.unpack("<I", reader.read(4))[0]
    states_nbt = reader.read(l)

    return (
        name,
        unmarshalNBT.UnMarshalBufferToPythonNBTObject(BytesIO(states_nbt))[0],  # type: ignore
        True,
    )


def state_to_runtime_id(
    block_name: str, block_states: nbtlib.tag.Compound
) -> tuple[int, bool]:
    writer = BytesIO()
    marshalNBT.MarshalPythonNBTObjectToWriter(writer, block_states, "")

    payload = as_python_bytes(
        LIB.StateToRuntimeID(as_c_string(block_name), as_c_bytes(writer.getvalue()))
    )
    reader = BytesIO(payload)

    if reader.read(1) == b"\x00":
        return (0, False)

    return (struct.unpack("<I", reader.read(4))[0], True)
