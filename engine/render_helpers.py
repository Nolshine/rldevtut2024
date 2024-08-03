from __future__ import annotations

import numpy as np
import tcod.console
import tcod.ecs.registry
import tcod.ecs.entity

from constants.tags import IsActor, IsPlayer, InMap, ActiveMap
from constants.game_constants import SCREEN_W, SCREEN_H
from components.components import Position, Graphic, MapShape, Tiles, VisibleTiles, ExploredTiles
from dungeon.tiles import TILES



def render_all_entities(root_console: tcod.console.Console, world: tcod.ecs.Registry, player: tcod.ecs.Entity) -> None:
    actor_drawn = set()
    for entity in world.Q.all_of(components=[Position, Graphic], relations=[(InMap, world[None].relation_tag[ActiveMap])]):
        if IsPlayer in entity.tags:
            continue # Always draw player last
        if entity.components[Position].raw in actor_drawn:
            continue # Do not draw over actor
        if IsActor in entity.tags:
            actor_drawn.add(entity.components[Position].raw)
        render_entity(root_console, entity)
    render_entity(root_console, player)

def render_entity(root_console: tcod.console.Console, entity: tcod.ecs.Entity) -> None:
    x, y = entity.components[Position].raw
    if not (0 <= x < SCREEN_W and 0 <= y < SCREEN_H):
        return
    visible = entity.relation_tag[InMap].components[VisibleTiles]
    if not visible[x, y]:
        return
    graphic = entity.components[Graphic]
    root_console.print(x, y, graphic.char, graphic.fg)

def render_map(console: tcod.console.Console, map_: tcod.ecs.Entity) -> None:
    shape = map_.components[MapShape]
    tiles = map_.components[Tiles]
    explored = map_.components[ExploredTiles]
    visible = map_.components[VisibleTiles]
    not_visible = ~visible

    console.rgb[:shape.width, :shape.height] = TILES["graphic"][np.where(visible, tiles, explored)]
    console.rgb["fg"][:shape.width, :shape.height][not_visible] //= 2
