from __future__ import annotations

from typing import Tuple, Final

import numpy as np
from numpy.typing import NDArray



class Position:
    """An entity's position on a map."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Position | Tuple[int, int]) -> Position:
        """Return a new position, offset by 'other'."""
        if isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else: # Stops mypy from yelling :P
            return self.__class__(self.x + other.x, self.y + other.y)
    
class Graphic:
    """An entity's visual representation."""
    def __init__(self, char: str, fg: Tuple[int, int, int]):
        self.char = char
        self.fg = fg

class MapShape:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

Tiles: Final = ("Tiles", NDArray[np.int8])