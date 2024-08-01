from __future__ import annotations

from typing import Final

import numpy as np
from numpy.typing import NDArray



class Position:
    """An entity's position on a map."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Position | tuple[int, int]) -> Position:
        """Return a new position, offset by 'other'."""
        if isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else: # Stops mypy from yelling :P
            return self.__class__(self.x + other.x, self.y + other.y)
        
    @property
    def raw(self) -> tuple[int, int]:
        return (self.x, self.y)
    
class Graphic:
    """An entity's visual representation."""
    def __init__(self, char: str, fg: tuple[int, int, int]):
        self.char = char
        self.fg = fg

class MapShape:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def raw(self) -> tuple[int, int]:
        return (self.width, self.height)
    
Name: Final = ("Name", str)

Tiles: Final = ("Tiles", NDArray[np.int8])
VisibleTiles: Final = ("VisibleTiles", NDArray[np.bool])
ExploredTiles: Final = ("ExploredTiles", NDArray[np.int8])