from __future__ import annotations

from itertools import pairwise
from typing import Iterator, List

import numpy as np
import scipy.ndimage as ndi
from numpy.typing import NDArray
import tcod
import tcod.ecs

from components.components import Tiles, VisibleTiles, ExploredTiles, Position, MapShape
from dungeon.tiles import TileIndices
from constants.map_constants import CA_FIRST_PASSES, CA_SECOND_PASSES, CA_MIN_WALLS, CA_MIN_FLOORS
from constants.tags import IsPlayer, InMap

import random



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
    
def flood_fill(map_tiles: NDArray[np.int8], start: tuple[int, int]) -> List[tuple[int, int]]:
    offsets: list[tuple[int, int]] = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    shape: tuple[int, ...] = map_tiles.shape

    orphan_tiles: List[tuple[int, int]] = []
    for x in range(shape[0]):
        for y in range(shape[1]):
            orphan_tiles.append((x, y))

    tiles: List[tuple[int, int]] = [] # the stack

    tiles.append(start)

    while (len(tiles) > 0):
        cur_tile: tuple[int, int] = tiles.pop()

        if cur_tile not in orphan_tiles:
            continue

        orphan_tiles.remove(cur_tile)
        cur_tile_index = map_tiles[*cur_tile]

        if cur_tile_index == TileIndices.WALL:
            continue

        for offset in offsets:
            x, y = cur_tile[0] + offset[0], cur_tile[1] + offset[1]
            if not ((0 <= x < shape[0]) and (0 <= y < shape[1])):
                continue
            tiles.append((x, y))

        # make sure no walls are left in the orphan list
        for tile_coord in orphan_tiles:
            if map_tiles[*tile_coord] == TileIndices.WALL:
                orphan_tiles.remove(tile_coord)
    
    return orphan_tiles

def generate_dungeon(
        world: tcod.ecs.Registry,
        map_width: int,
        map_height: int,
        room_max_size: int,
        room_min_size: int,
        max_rooms: int,
) -> tcod.ecs.Entity:
    rng = world[None].components["Random"]
    (player,) = world.Q.all_of(tags=[IsPlayer])

    map_ = world[object()]
    shape = MapShape(map_width, map_height)
    map_.components[Tiles] = np.full(shape.raw, TileIndices.WALL, dtype=np.int8)
    map_.components[VisibleTiles] = np.zeros(shape.raw, dtype=np.bool)
    map_.components[ExploredTiles] = np.full(shape.raw, TileIndices.VOID, dtype=np.int8)
    map_.components[MapShape] = shape
    map_tiles = map_.components[Tiles]

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = rng.randint(room_min_size, room_max_size)
        room_height = rng.randint(room_min_size, room_max_size)

        x = rng.randint(0, shape.width - room_width - 1)
        y = rng.randint(0, shape.height - room_height - 1)

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
            for x, y in tunnel_between(world, rooms[-1].center, new_room.center):
                map_tiles[x, y] = TileIndices.FLOOR
        
        rooms.append(new_room)
    
    return map_

def generate_caves(
        world: tcod.ecs.Registry,
        map_width: int,
        map_height: int,
        room_max_size: int,
        room_min_size: int,
        max_rooms: int,
        seed: int | None = None,
) -> tcod.ecs.Entity:
    print("Generating caves...")
    rng = world[None].components["Random"]
    map_ = generate_dungeon(world, map_width, map_height, room_max_size, room_min_size, max_rooms)
    shape = map_.components[MapShape]
    map_tiles = map_.components[Tiles]
    map_tiles2 = np.copy(map_.components[Tiles])

    # add random noise to walls
    for x in range(shape.width):
        for y in range(shape.height):
            if x == 0 or y == 0 or x == shape.width -1 or y == shape.height-1:
                continue
            if (map_tiles[x, y] == TileIndices.WALL) and rng.random() < 0.55:
                map_tiles2[x, y] = TileIndices.FLOOR
    map_tiles = map_tiles2

    # apply CA to grow cave walls
    for i in range(CA_FIRST_PASSES):
        map_tiles = cave_first_ca(map_tiles, shape)
    
    for i in range(CA_SECOND_PASSES):
        map_tiles = cave_second_ca(map_tiles, shape)

    s = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]

    # create a list of slices that represent unconnected regions
    # must make a copy that adjusts wall to be the 'background', in other words wall tiles are 0
    # adjusted = map_tiles-1
    labelled, num_features = ndi.label(map_tiles, structure=s)
    regions: list[tuple[slice, slice, None]] = ndi.find_objects(labelled)
    isolated: list[tuple[slice, slice, None]] = []
    assert len(regions) == num_features


    for region_slices in regions:
        region = map_tiles[region_slices[0], region_slices[1]]
        region_width, region_height = (len(region), len(region[0]))
        if (region_width < room_min_size) or (region_height < room_min_size):
            # wall in regions that are too small
            map_tiles[region_slices[0], region_slices[1]] = np.where(
                map_tiles[region_slices[0], region_slices[1]] == TileIndices.FLOOR,
                TileIndices.DEBUG,
                map_tiles[region_slices[0], region_slices[1]]
            )
        else:
            # add big regions to a list
            isolated.append(region_slices)

    # connect isolated regions
    for r1, r2 in pairwise(isolated):
        print("connecting regions:") # TODO: Remove when done testing
        print(f"{r1} / {r2}") # Remove when done testing
        good = False
        while not good:
            good = True
            x1, y1 = rng.randint(r1[0].start, r1[0].stop - 1), rng.randint(r1[1].start, r1[1].stop - 1)
            x2, y2 = rng.randint(r2[0].start, r2[0].stop - 1), rng.randint(r2[1].start, r2[1].stop - 1)
            if map_tiles[x1, y1] == TileIndices.WALL or map_tiles[x2, y2] == TileIndices.WALL:
                good = False
        for x, y in tunnel_between(world, (x1, y1), (x2, y2)): # TODO: more organic tunneling function
            map_tiles[x, y] = TileIndices.FLOOR


    map_.components[Tiles] = map_tiles

    return map_

def cave_first_ca(tiles_input: NDArray[np.int8], shape: MapShape) -> NDArray[np.int8]:
    tiles_output = np.copy(tiles_input)
    for x in range(shape.width):
        for y in range(shape.height):
            if check_neighbors(tiles_input, (x, y), shape, TileIndices.WALL, False) >= CA_MIN_WALLS:
                tiles_output[x, y] = TileIndices.WALL
    return tiles_output

def cave_second_ca(tiles_input: NDArray[np.int8], shape: MapShape) -> NDArray[np.int8]:
    tiles_output = np.copy(tiles_input)
    for x in range(shape.width):
        for y in range(shape.height):
            if check_neighbors(tiles_input, (x, y), shape, TileIndices.FLOOR, True) >= CA_MIN_FLOORS:
                tiles_output[x, y] = TileIndices.FLOOR
    return tiles_output

def check_neighbors(
        tiles: NDArray[np.int8],
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
        world: tcod.ecs.Registry,
        start: tuple[int, int],
        end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    rng = world[None].components["Random"]
    x1, y1 = start
    x2, y2 = end
    if rng.random()  < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y