import nbtlib
from ..internal.symbol_export_conversion import state_to_runtime_id
from ..world.define import BlockStates, Dimension, Range

EMPTY_COMPOUND = nbtlib.tag.Compound()
EMPTY_BLOCK_STATES = EMPTY_COMPOUND

DIMENSION_ID_OVERWORLD = 0
DIMENSION_ID_NETHER = 1
DIMENSION_ID_END = 2

DIMENSION_OVERWORLD = Dimension(DIMENSION_ID_OVERWORLD)
DIMENSION_NETHER = Dimension(DIMENSION_ID_NETHER)
DIMENSION_END = Dimension(DIMENSION_ID_END)

RANGE_OVERWORLD = DIMENSION_OVERWORLD.range()
RANGE_NETHER = DIMENSION_NETHER.range()
RANGE_END = DIMENSION_END.range()
RANGE_INVALID = Range(0, -1)

AIR_BLOCK_STATES = BlockStates("minecraft:air")
AIR_BLOCK_RUNTIME_ID = state_to_runtime_id("minecraft:air", EMPTY_BLOCK_STATES)[0]
