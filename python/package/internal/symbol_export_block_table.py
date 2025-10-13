from io import BytesIO
import struct
import nbtlib
from .types import LIB
from .types import CSlice, CString, CInt, CLongLong
from .types import as_c_bytes, as_python_bytes, as_c_string, as_python_string
from ..utils import marshalNBT, unmarshalNBT


LIB.NewBlockTable.argtypes = [CInt]
LIB.ReleaseBlockTable.argtypes = [CLongLong]
LIB.Table_AirRuntimeID.argtypes = [CLongLong]
LIB.Table_UseNetworkIDHashes.argtypes = [CLongLong]
LIB.Table_RuntimeIDToState.argtypes = [CLongLong, CInt]
LIB.Table_StateToRuntimeID.argtypes = [CLongLong, CString, CSlice]
LIB.Table_RegisterCustomBlock.argtypes = [CLongLong, CString, CSlice, CInt]
LIB.Table_RegisterPermutation.argtypes = [CLongLong, CString, CInt, CSlice]
LIB.Table_FinaliseRegister.argtypes = [CLongLong]

LIB.NewBlockTable.restype = CLongLong
LIB.ReleaseBlockTable.restype = None
LIB.Table_AirRuntimeID.restype = CInt
LIB.Table_UseNetworkIDHashes.restype = CInt
LIB.Table_RuntimeIDToState.restype = CSlice
LIB.Table_StateToRuntimeID.restype = CSlice
LIB.Table_RegisterCustomBlock.restype = CString
LIB.Table_RegisterPermutation.restype = CString
LIB.Table_FinaliseRegister.restype = CString


def new_block_table(use_network_id_hashes: bool) -> int:
    return int(LIB.NewBlockTable(CInt(use_network_id_hashes)))


def release_block_table(id: int) -> None:
    LIB.ReleaseBlockTable(CLongLong(id))


def table_air_runtime_id(id: int) -> int:
    return int(LIB.Table_AirRuntimeID(CLongLong(id)))


def table_use_network_id_hashes(id: int) -> int:
    return int(LIB.Table_UseNetworkIDHashes(CLongLong(id)))


def table_runtime_id_to_state(
    id: int, block_runtime_id: int
) -> tuple[str, nbtlib.tag.Compound | None, bool]:
    payload = as_python_bytes(
        LIB.Table_RuntimeIDToState(CLongLong(id), CInt(block_runtime_id))
    )
    reader = BytesIO(payload)

    if reader.read(1) == b"\x00":
        return "", None, False

    length: int = struct.unpack("<H", reader.read(2))[0]
    name = reader.read(length).decode(encoding="utf-8")

    length = struct.unpack("<I", reader.read(4))[0]
    states_nbt = reader.read(length)

    return (
        name,
        unmarshalNBT.UnMarshalBufferToPythonNBTObject(BytesIO(states_nbt))[0],  # type: ignore
        True,
    )


def table_state_to_runtime_id(
    id: int, block_name: str, block_states: nbtlib.tag.Compound
) -> tuple[int, bool]:
    writer = BytesIO()
    marshalNBT.MarshalPythonNBTObjectToWriter(writer, block_states, "")

    payload = as_python_bytes(
        LIB.Table_StateToRuntimeID(
            CLongLong(id), as_c_string(block_name), as_c_bytes(writer.getvalue())
        )
    )
    reader = BytesIO(payload)

    if reader.read(1) == b"\x00":
        return 0, False
    return struct.unpack("<I", reader.read(4))[0], True


def table_register_custom_block(
    id: int, block_name: str, block_states: nbtlib.tag.Compound, block_version: int
) -> str:
    writer = BytesIO()
    marshalNBT.MarshalPythonNBTObjectToWriter(writer, block_states, "")
    return as_python_string(
        LIB.Table_RegisterCustomBlock(
            CLongLong(id),
            as_c_string(block_name),
            as_c_bytes(writer.getvalue()),
            CInt(block_version),
        )
    )


def table_register_permutation(
    id: int,
    block_name: str,
    block_version: int,
    states_enum: list[
        tuple[
            str, list[nbtlib.tag.Byte] | list[nbtlib.tag.Int] | list[nbtlib.tag.String]
        ]
    ],
) -> str:
    writer = BytesIO()
    writer.write(len(states_enum).to_bytes(length=1, signed=False))

    for state_key_name, possible_values in states_enum:
        writer.write(struct.pack("<H", len(state_key_name)))
        writer.write(state_key_name.encode(encoding="utf-8"))

        writer.write(len(possible_values).to_bytes(length=1, signed=False))
        if len(possible_values) == 0:
            continue

        if isinstance(possible_values[0], nbtlib.tag.Byte):
            writer.write(b"\x00")
            for value in possible_values:
                assert isinstance(value, nbtlib.tag.Byte)
                writer.write(value.to_bytes(length=1, signed=False))
        if isinstance(possible_values[0], nbtlib.tag.Int):
            writer.write(b"\x00")
            for value in possible_values:
                assert isinstance(value, nbtlib.tag.Int)
                writer.write(struct.pack("<i", value))
        if isinstance(possible_values[0], nbtlib.tag.String):
            writer.write(b"\x00")
            for value in possible_values:
                assert isinstance(value, nbtlib.tag.String)
                writer.write(struct.pack("<H", len(value)))
                writer.write(value.encode(encoding="utf-8"))

    return as_python_string(
        LIB.Table_RegisterPermutation(
            CLongLong(id),
            as_c_string(block_name),
            CInt(block_version),
            as_c_bytes(writer.getvalue()),
        )
    )


def table_finalise_register(id: int) -> str:
    return as_python_string(LIB.Table_FinaliseRegister(CLongLong(id)))
