from __future__ import annotations

from typing import Reversible

import numpy as np
import tcod.console
import tcod.ecs.registry
import tcod.ecs.entity

import constants.colors as colors
from constants.tags import IsActor, IsPlayer, InMap, ActiveMap
from constants.game_constants import SCREEN_W, SCREEN_H
from constants.gui_constants import HEALTH_BAR_WIDTH, MESSAGE_LOG_WIDTH, MESSAGE_LOG_HEIGHT
from components.main import (
    Position,
    Graphic,
    MapShape,
    Tiles,
    VisibleTiles,
    ExploredTiles,
    HP,
    HPMax,
)
from components.message_log import MessageLog, Message
from dungeon.tiles import TILES



def render_all_entities(console: tcod.console.Console, world: tcod.ecs.Registry) -> None:
    (player,) = world.Q.all_of(tags=[IsPlayer])
    actor_drawn = set()
    for entity in world.Q.all_of(components=[Position, Graphic], relations=[(InMap, world[None].relation_tag[ActiveMap])]):
        if IsPlayer in entity.tags:
            continue # Always draw player last
        if entity.components[Position].raw in actor_drawn:
            continue # Do not draw over actor
        if IsActor in entity.tags:
            actor_drawn.add(entity.components[Position].raw)
        render_entity(console, entity)
    render_entity(console, player)

def render_entity(console: tcod.console.Console, entity: tcod.ecs.Entity) -> None:
    x, y = entity.components[Position].raw
    if not (0 <= x < SCREEN_W and 0 <= y < SCREEN_H):
        return
    visible = entity.relation_tag[InMap].components[VisibleTiles]
    if not visible[x, y]:
        return
    graphic = entity.components[Graphic]
    console.print(x, y, graphic.char, graphic.fg)

def render_map(console: tcod.console.Console, world: tcod.ecs.Registry) -> None:
    map_ = world[None].relation_tag[ActiveMap]
    shape = map_.components[MapShape]
    tiles = map_.components[Tiles]
    explored = map_.components[ExploredTiles]
    visible = map_.components[VisibleTiles]
    not_visible = ~visible

    console.rgb[:shape.width, :shape.height] = TILES["graphic"][np.where(visible, tiles, explored)]
    console.rgb["fg"][:shape.width, :shape.height][not_visible] //= 2

def render_bar(
        console: tcod.console.Console,
        current_val: int,
        max_val: int,
        total_width: int,
) -> None:
    bar_width = int(float(current_val) / max_val * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=colors.BAR_EMPTY)
    if bar_width > 0:
        console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=colors.BAR_FILLED)

    console.print(x=1, y=45, string=f"HP: {current_val}/{max_val}", fg=colors.WHITE)

def render_messages(
        world: tcod.ecs.Registry,
        width: int,
        height: int,
) -> tcod.console.Console:
    """Return a console with the message log rendered onto it..
    
    Messages are rendered starting at the last entry and working back."""
    messages: Reversible[Message] = world[None].components[MessageLog]
    console = tcod.console.Console(width, height)

    y = height

    for message in reversed(messages):
        y -= tcod.console.get_height_rect(width, message.full_text)
        console.print_box(x=0, y=y, width=width, height=height, string=message.full_text, fg=message.fg)
        if y <= 0:
            break
    return console

def render_main(console: tcod.console.Console, world: tcod.ecs.Registry):
    (player,) = world.Q.all_of(tags=[IsPlayer])
    render_map(console, world)
    render_all_entities(console, world)
    render_bar(console, player.components[HP], player.components[HPMax], HEALTH_BAR_WIDTH)
    render_messages(world, width=MESSAGE_LOG_WIDTH, height=MESSAGE_LOG_HEIGHT).blit(console, dest_x=21, dest_y=45)