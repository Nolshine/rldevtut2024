from __future__ import annotations
from typing import Tuple
from enum import IntEnum, auto

import numpy as np
import tcod.console

import constants.colors as colors



TILES = np.asarray(
    [
        ("wall", (ord("#"), colors.DARK_FADED_BROWN, colors.BLACK), 0, False),
        ("floor", (ord("."), colors.DARK_GREY, colors.BLACK), 1, True),
    ],
    dtype=[
        ("name", str),
        ("graphic", tcod.console.rgb_graphic),
        ("walk_cost", np.int8),
        ("transparent", bool),
    ],
)
TILES.flags.writeable = False

class TileIndices(IntEnum):
    WALL=0 # First value in list HAS to be set to zero, as default IntEnum numbering starts at 1
    FLOOR=auto()

print(TileIndices.WALL)
