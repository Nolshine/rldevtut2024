from __future__ import annotations

import random
from typing import Iterator, List

import numpy as np
import tcod.ecs

from components.components import Tiles, Position, MapShape
from dungeon.tiles import TileIndices
from constants.tags import IsPlayer, InMap



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
    
    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    

def generate_dungeon(
        world: tcod.ecs.Registry,
        map_width: int,
        map_height: int,
        room_max_size: int,
        room_min_size: int,
        max_rooms: int,
) -> tcod.ecs.Entity:
    (player,) = world.Q.all_of(tags=[IsPlayer])
    (npc,) = world.Q.all_of(tags=["Npc"])

    map_ = world[object()]
    shape = MapShape(map_width, map_height)
    map_.components[Tiles] = np.zeros((map_width, map_height), dtype=np.int8)
    map_.components[MapShape] = shape
    map_tiles = map_.components[Tiles]

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, shape.width - room_width - 1)
        y = random.randint(0, shape.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # discard room if it intersects another room
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        map_tiles[new_room.inner] = TileIndices.FLOOR

        if len(rooms) == 0:
            # First room, place player
            player.components[Position] = Position(*new_room.center)
            player.relation_tag[InMap] = map_
        else:
            # All other rooms after the first
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                map_tiles[x, y] = TileIndices.FLOOR
        
        rooms.append(new_room)

    # for testing
    npc.components[Position] = Position(*rooms[-1].center)
    npc.relation_tag[InMap] = map_
    
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