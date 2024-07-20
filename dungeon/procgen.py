from __future__ import annotations

import random
from typing import Iterator, List

import numpy as np
import tcod.ecs

from components.components import Tiles, Position, MapShape
from dungeon.tiles import TileIndices
from constants.map_constants import CA_FIRST_PASSES, CA_SECOND_PASSES, CA_MIN_WALLS, CA_MIN_FLOORS
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
    (npc,) = world.Q.all_of(tags=["Npc"]) # TODO: remove outside of testing builds

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

def generate_caves(
        world: tcod.ecs.Registry,
        map_width: int,
        map_height: int,
        room_max_size: int,
        room_min_size: int,
        max_rooms: int,
) -> tcod.ecs.Entity:
    map_ = generate_dungeon(world, map_width, map_height, room_max_size, room_min_size, max_rooms)
    shape = map_.components[MapShape]
    map_tiles = map_.components[Tiles]
    map_tiles2 = np.copy(map_.components[Tiles])

    # add random noise to walls
    for x in range(shape.width):
        for y in range(shape.height):
            if x == 0 or y == 0 or x == shape.width -1 or y == shape.height-1:
                continue
            if (map_tiles[x, y] == TileIndices.WALL) and random.random() < 0.55:
                map_tiles2[x, y] = TileIndices.FLOOR
    map_tiles = map_tiles2

    # apply CA to grow cave walls
    for i in range(CA_FIRST_PASSES):
        map_tiles = cave_first_ca(map_tiles, shape)
    
    for i in range(CA_SECOND_PASSES):
        map_tiles = cave_second_ca(map_tiles, shape)

    map_.components[Tiles] = map_tiles

    return map_

def cave_first_ca(tiles_input: np.ndarray[np.int8], shape: MapShape):
    tiles_output = np.copy(tiles_input)
    for x in range(shape.width):
        for y in range(shape.height):
            if check_neighbors(tiles_input, (x, y), shape, TileIndices.WALL, False) >= CA_MIN_WALLS:
                tiles_output[x, y] = TileIndices.WALL
    return tiles_output

def cave_second_ca(tiles_input: np.ndarray[np.int8], shape: MapShape):
    tiles_output = np.copy(tiles_input)
    for x in range(shape.width):
        for y in range(shape.height):
            if check_neighbors(tiles_input, (x, y), shape, TileIndices.FLOOR, True) >= CA_MIN_FLOORS:
                tiles_output[x, y] = TileIndices.FLOOR
    return tiles_output

def check_neighbors(
        tiles: np.ndarray[np.int8],
        point: tuple[int, int], 
        shape: MapShape,
        tile_type: TileIndices,
        ignore_edges: bool,
    ) -> int:
    x, y = point
    offsets = (-1, 0, 1)
    count = 0
    for i in offsets:
        for j in offsets:
                cur_x = x + i
                cur_y = y + j
                if not ((0 <= cur_x < shape.width) and (0 <= cur_y < shape.height)):
                    if not ignore_edges:
                        count += 1
                    continue
                if tiles[cur_x, cur_y] == tile_type:
                    count += 1
    return count

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