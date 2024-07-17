from __future__ import annotations
from typing import Any

import tcod.ecs

from components.components import Position

class Move:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, entity: tcod.ecs.Entity) -> None:
        entity.components[Position] += (self.dx, self.dy)

def escape_action(entity: tcod.ecs.Entity) -> None:
    raise SystemExit()