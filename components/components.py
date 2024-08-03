from __future__ import annotations

from typing import Final

import attrs
import numpy as np
from numpy.typing import NDArray

import tcod.ecs
import tcod.ecs.callbacks

from actions.action import Action


@attrs.define(frozen=True)
class Position:
    """An entity's position on a map."""
    x: int
    y: int

    def __add__(self, other: Position | tuple[int, int]) -> Position:
        """Return a new position, offset by 'other'."""
        if isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else: # Stops mypy from yelling :P
            return self.__class__(self.x + other.x, self.y + other.y)
        
    @property
    def raw(self) -> tuple[int, int]:
        return (self.x, self.y)
    
@attrs.define(frozen=True)
class Graphic:
    """An entity's visual representation."""
    char: str
    fg: tuple[int, int, int]

class MapShape:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def raw(self) -> tuple[int, int]:
        return (self.width, self.height)
    
Name: Final = ("Name", str)
"""An entity's name."""
HP: Final = ("HP", int)
"""An actor's current hitpoints."""
HPMax: Final = ("Max_HP", int)
"""An actor's maximum hitpoints."""
PowerMin: Final = ("PowerMin", int)
"""An entity's minimum damage."""
PowerMax: Final = ("PowerMax", int)
"""An entity's maximum damage."""
Defense: Final = ("Defense", int)
"""An entity's armor value."""
AI: Final = ("AI", Action)
"""An actor's AI action."""

Tiles: Final = ("Tiles", NDArray[np.int8])
"""A map's tile composition."""
VisibleTiles: Final = ("VisibleTiles", NDArray[np.bool])
"""A player's currently visible tiles."""
ExploredTiles: Final = ("ExploredTiles", NDArray[np.int8])
"""A map's tiles that have already been seen."""

@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(e: tcod.ecs.Entity, old: Position | None, new: Position | None) -> None:
    if old == new:
        return
    if old is not None:
        e.tags.remove(old)
    if new is not None:
        e.tags.add(new)