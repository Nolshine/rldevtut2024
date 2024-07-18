from __future__ import annotations
from typing import Tuple

import numpy as np
import tcod.console
import tcod.ecs.registry
import tcod.ecs.entity

from constants.tags import IsPlayer
from constants.game_constants import SCREEN_W, SCREEN_H
from components.components import Position, Graphic, MapShape, Tiles
from levels.tiles import TILES



def render_all_entities(root_console: tcod.console.Console, world: tcod.ecs.Registry, player: tcod.ecs.Entity) -> None:
    for entity in world.Q.all_of(components=[Position, Graphic]):
        if IsPlayer in entity.tags:
            continue
        render_entity(root_console, entity)
    render_entity(root_console, player)

def render_entity(root_console: tcod.console.Console, entity: tcod.ecs.Entity) -> None:
    pos = entity.components[Position]
    if not (0 <= pos.x < SCREEN_W and 0 <= pos.y < SCREEN_H):
        return
    graphic = entity.components[Graphic]
    root_console.print(pos.x, pos.y, graphic.char, graphic.fg)

def create_actor(x: int, y: int, char: str, fg: Tuple[int, int, int], world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    entity = world[object()]
    entity.components[Position] = Position(x, y)
    entity.components[Graphic] = Graphic(char, fg)
    return entity

def render_map(console: tcod.console.Console, world: tcod.ecs.Registry, map_: tcod.ecs.Entity) -> None:
    tile_indices = map_.components[Tiles]
    shape = map_.components[MapShape]
    console.rgb[0:shape.width, 0:shape.height] = TILES["graphic"][map_.components[Tiles]]