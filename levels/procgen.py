from __future__ import annotations

import random
from typing import Iterator

import numpy as np
import tcod.ecs

from components.components import Tiles, Position, MapShape
from levels.tiles import TileIndices
from constants.tags import IsPlayer



class RectangularRoom:
    """A rectangular room."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y
    
    @property
    def inner(self) -> tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    

def generate_dungeon(world: tcod.ecs.Registry, map_width: int, map_height: int) -> tcod.ecs.Entity:
    # new map
    map_ = world[object()]
    map_.components[Tiles] = np.zeros((map_width, map_height), dtype=np.int8)
    map_.components[MapShape] = MapShape(map_width, map_height)
    map_tiles = map_.components[Tiles]

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    map_tiles[room_1.inner] = TileIndices.FLOOR
    map_tiles[room_2.inner] = TileIndices.FLOOR

    for x, y in tunnel_between(room_1.center, room_2.center):
        map_tiles[x, y] = TileIndices.FLOOR

    (player,) = world.Q.all_of(tags=[IsPlayer])
    (npc,) = world.Q.all_of(tags=["Npc"])
    player.components[Position] = Position(*room_1.center)
    npc.components[Position] = Position(*room_2.center)

    return map_

def tunnel_between(
        start: tuple[int, int],
        end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random()  < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y