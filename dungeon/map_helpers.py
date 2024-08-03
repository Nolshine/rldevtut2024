from __future__ import annotations

from typing import Iterator, TYPE_CHECKING
from random import Random

import numpy as np
from numpy.typing import NDArray

import tcod
import tcod.ecs

import mobs.entity_prefabs as prefabs
from components.components import Position, Tiles, AI
from constants.map_constants import MAX_MONSTERS_PER_ROOM
from constants.tags import InMap, IsActor
from dungeon.tiles import TileIndices
from engine.actor_helpers import create_actor
from actions.actions import SimpleEnemy

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


def tunnel_between(
        world: tcod.ecs.Registry,
        start: tuple[int, int],
        end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    rng: Random = world[None].components["Random"]
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


def place_monsters_in_rooms(map_: tcod.ecs.Entity, rooms: list[RectangularRoom], world: tcod.ecs.Registry) -> None:
    rng: Random = world[None].components["Random"]
    map_tiles: NDArray[np.int8] = map_.components[Tiles]
    for i in range(len(rooms)):
    # for i in range(1):
        if i == 0:
            # no monsters in the antechamber
            continue
        for j in range(MAX_MONSTERS_PER_ROOM):
        # for i in range(1):
            entities = world.Q.all_of(tags=[IsActor], relations=[(InMap, map_)])
            x, y = rng.randint(rooms[i].x1 + 1, rooms[i].x2), rng.randint(rooms[i].y1 + 1, rooms[i].y2)
            if ((not map_tiles[x, y] == TileIndices.WALL) and
                (not any(e.components[Position].raw == (x, y) for e in entities))):
                new_actor: tcod.ecs.Entity
                prefab: prefabs.EntityPrefab
                if rng.random() < 0.8:
                    prefab = prefabs.orc
                else:
                    prefab = prefabs.troll
                new_actor = create_actor((x, y), prefab, world)
                new_actor.components[AI] = SimpleEnemy()
                new_actor.relation_tag[InMap] = map_