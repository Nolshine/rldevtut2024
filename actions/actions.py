from __future__ import annotations
from typing import Any

import tcod.ecs

from constants.game_constants import SCREEN_W, SCREEN_H
from constants.map_constants import *
from constants.tags import ActiveMap
from components.components import Position
from dungeon.procgen import generate_caves

class Move:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, entity: tcod.ecs.Entity) -> None:
        entity.components[Position] += (self.dx, self.dy)

def escape_action(entity: tcod.ecs.Entity) -> None:
    raise SystemExit()

def regenenerate_map(entity: tcod.ecs.Entity) -> None: # TODO: remove when not in testing builds
    r = entity.registry
    map_ = generate_caves(
        r,
        SCREEN_W,
        SCREEN_H,
        ROOM_MAX_SIZE,
        ROOM_MIN_SIZE,
        MAX_ROOMS,
    )
    r[None].relation_tag[ActiveMap] = map_