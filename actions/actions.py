from __future__ import annotations

from random import Random
import time
from typing import Any

import tcod.ecs

from constants.game_constants import SCREEN_W, SCREEN_H
from constants.map_constants import *
from constants.tags import ActiveMap
from components.components import Position, Tiles
from dungeon.procgen import generate_caves
from dungeon.tiles import TileIndices

class Move:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, e: tcod.ecs.Entity) -> None:
        pos = e.components[Position]
        target = Position(pos.x + self.dx, pos.y + self.dy)
        map_tiles = e.registry[None].relation_tag[ActiveMap].components[Tiles]
        if not map_tiles[target.x, target.y] == TileIndices.WALL:
            e.components[Position] = target

def escape_action(entity: tcod.ecs.Entity) -> None:
    raise SystemExit()

def regenenerate_map(entity: tcod.ecs.Entity) -> None: # TODO: remove when not in testing builds
    new_seed = int(time.time())
    print(f"Seed: {new_seed}")
    r = entity.registry
    r[None].components["Random"].seed(new_seed)
    map_ = generate_caves(
        r,
        SCREEN_W,
        SCREEN_H,
        ROOM_MAX_SIZE,
        ROOM_MIN_SIZE,
        MAX_ROOMS,
    )
    r[None].relation_tag[ActiveMap] = map_