from __future__ import annotations

from typing import Final

import attrs
import numpy as np
from numpy.typing import NDArray

import tcod.ecs
import tcod.ecs.callbacks

from actions.action import Action



class Component:
    ...

# map components
@attrs.define
class MapShape(Component):
    width: int
    height: int

    @property
    def as_tuple(self) -> tuple[int, int]:
        return (self.width, self.height)

Tiles: Final = ("Tiles", NDArray[np.int8])
"""A map's tile composition."""
VisibleTiles: Final = ("VisibleTiles", NDArray[np.bool])
"""A player's currently visible tiles."""
ExploredTiles: Final = ("ExploredTiles", NDArray[np.int8])
"""A map's tiles that have already been seen."""

# Entity/Actor components
@attrs.define(frozen=True)
class Position(Component):
    """An entity's position on a map."""
    x: int
    y: int

    def __add__(self, other: Position | tuple[int, int]) -> Position:
        """Return a new position, offset by 'other'."""
        if isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else:
            return self.__class__(self.x + other.x, self.y + other.y)

    @property
    def packed(self) -> tuple[int, int]:
        return (self.x, self.y)

@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(e: tcod.ecs.Entity, old: Position | None, new: Position | None) -> None:
    if old == new:
        return
    if old is not None:
        e.tags.remove(old)
    if new is not None:
        e.tags.add(new)

@attrs.define(frozen=True)
class Graphic(Component):
    """An entity's visual representation."""
    char: str
    fg: tuple[int, int, int]

@attrs.define
class Inventory(Component):
    """Represent's the existence and size of an entity's inventory."""
    size: int
    max_size: int

@attrs.define
class HP(Component):
    """An actor's current hitpoints."""
    value: int

@attrs.define
class HPMax(Component):
    """An actor's maximum hitpoints."""
    value: int

@attrs.define
class Power(Component):
    """An entity's minimum damage."""
    min: int
    max: int

@attrs.define
class Defense(Component):
    """An entity's armor value."""
    value: int

@attrs.define
class AI(Component):
    """An actor's AI action."""
    action: Action

Name: Final = ("Name", str)

# Effects (healing, poison, etc)

@attrs.define
class Healing(Component):
    """A healing effect """
    amount: int
