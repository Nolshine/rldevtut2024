from __future__ import annotations

from typing import Reversible

import numpy as np
import tcod.console

import constants.colors as colors
from constants.tags import IsActor, IsPlayer, InMap, ActiveMap
from constants.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from constants.gui_constants import (
    GUI_FRAME_DECORATION,
    GUI_FRAME_CROSS_CHARS,
    STAT_SECTION_Y,
    STAT_SECTION_HEIGHT,
    RESOURCE_SECTION_WIDTH,
    HEALTH_BAR_X,
    HEALTH_BAR_Y_OFFSET,
    HEALTH_BAR_WIDTH,
    MESSAGE_SECTION_X,
    MESSAGE_SECTION_Y,
    MESSAGE_SECTION_WIDTH,
    MESSAGE_LOG_X,
    MESSAGE_LOG_WIDTH,
    MESSAGE_LOG_HEIGHT,
    EXAMINE_SECTION_X,
    EXAMINE_SECTION_WIDTH,
)
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
    actor_drawn: set[tuple[int, int]] = set()
    for entity in world.Q.all_of(components=[Position, Graphic], relations=[(InMap, world[None].relation_tag[ActiveMap])]):
        if IsPlayer in entity.tags:
            continue # Always draw player last
        if entity.components[Position].packed in actor_drawn:
            continue # Do not draw over actor
        if IsActor in entity.tags:
            actor_drawn.add(entity.components[Position].packed)
        render_entity(console, entity)
    render_entity(console, player)

def render_entity(console: tcod.console.Console, entity: tcod.ecs.Entity) -> None:
    x, y = entity.components[Position].packed
    if not (0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT):
        return
    visible = entity.relation_tag[InMap].components[VisibleTiles]
    if not visible[x, y]:
        return
    graphic = entity.components[Graphic]
    console.print(x=x, y=y, text=graphic.char, fg=graphic.fg)

def render_map(world: tcod.ecs.Registry) -> tcod.console.Console:
    map_ = world[None].relation_tag[ActiveMap]
    shape = map_.components[MapShape]
    tiles = map_.components[Tiles]
    explored = map_.components[ExploredTiles]
    visible = map_.components[VisibleTiles]
    not_visible = ~visible
    console = tcod.console.Console(width=shape.width, height=shape.height, order="F")
    console.rgb[:shape.width, :shape.height] = TILES["graphic"][np.where(visible, tiles, explored)]
    console.rgb["fg"][:shape.width, :shape.height][not_visible] //= 2
    return console

def render_bar(
        x: int,
        y: int,
        console: tcod.console.Console,
        current_val: int,
        max_val: int,
        total_width: int,
) -> None:
    bar_width = int(float(current_val) / max_val * total_width)

    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=colors.BAR_EMPTY)
    if bar_width > 0:
        console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=colors.BAR_FILLED)
    bar_str = f"HP: {current_val}/{max_val}"
    console.print(x=x + 1, y=y, text=bar_str, fg=colors.WHITE)

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
        console.print(x=0, y=y, width=width, height=height, text=message.full_text, fg=message.fg)
        if y <= 0:
            break
    return console

def render_frames(console: tcod.console.Console) -> None:
    # resources frame
    console.draw_frame(
        x=0,
        y=STAT_SECTION_Y,
        width=RESOURCE_SECTION_WIDTH,
        height=STAT_SECTION_HEIGHT,
        fg=colors.GUI_FRAME_FG,
        decoration=GUI_FRAME_DECORATION,
        clear=False,
    )
    # message log frame
    console.draw_frame(
        x=MESSAGE_SECTION_X,
        y=MESSAGE_SECTION_Y,
        width=MESSAGE_SECTION_WIDTH,
        height=STAT_SECTION_HEIGHT,
        fg=colors.GUI_FRAME_FG,
        decoration=GUI_FRAME_DECORATION,
        clear=False,
    )
    # examine section frame
    console.draw_frame(
        x=EXAMINE_SECTION_X,
        y=STAT_SECTION_Y,
        width=EXAMINE_SECTION_WIDTH,
        height=STAT_SECTION_HEIGHT,
        fg=colors.GUI_FRAME_FG,
        decoration=GUI_FRAME_DECORATION,
        clear=False,
    )
    # screen-wide frame
    console.draw_frame(
        x=0,
        y=0,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        fg=colors.GUI_FRAME_FG,
        decoration=GUI_FRAME_DECORATION,
        clear=False,
    )
    # left side cross
    console.print(
        x=0,
        y=STAT_SECTION_Y,
        text=GUI_FRAME_CROSS_CHARS[0],
        fg=colors.GUI_FRAME_FG,
    )
    # right side cross
    console.print(
        x=SCREEN_WIDTH-1,
        y=STAT_SECTION_Y,
        text=GUI_FRAME_CROSS_CHARS[1],
        fg=colors.GUI_FRAME_FG,
    )
    # resource/messages top and bottom crosses
    console.print(
        x=MESSAGE_SECTION_X,
        y=STAT_SECTION_Y,
        text=GUI_FRAME_CROSS_CHARS[2],
        fg=colors.GUI_FRAME_FG,
    )
    console.print(
        x=MESSAGE_SECTION_X,
        y=SCREEN_HEIGHT-1,
        text=GUI_FRAME_CROSS_CHARS[3],
        fg=colors.GUI_FRAME_FG,
    )
    # messages/examine top and bottom crosses
    console.print(
        x=EXAMINE_SECTION_X,
        y=STAT_SECTION_Y,
        text=GUI_FRAME_CROSS_CHARS[2],
        fg=colors.GUI_FRAME_FG,
    )
    console.print(
        x=EXAMINE_SECTION_X,
        y=SCREEN_HEIGHT-1,
        text=GUI_FRAME_CROSS_CHARS[3],
        fg=colors.GUI_FRAME_FG,
    )


def render_main(console: tcod.console.Console, world: tcod.ecs.Registry) -> None:
    render_frames(console)
    (player,) = world.Q.all_of(tags=[IsPlayer])
    map_console = render_map(world)
    render_all_entities(map_console, world)
    map_console.blit(dest=console, dest_x=1, dest_y=1)
    bar_y = SCREEN_HEIGHT + HEALTH_BAR_Y_OFFSET
    render_bar(
        x=HEALTH_BAR_X,
        y=bar_y,
        console=console,
        current_val=player.components[HP],
        max_val=player.components[HPMax],
        total_width=HEALTH_BAR_WIDTH,
    )
    message_log_y = MESSAGE_SECTION_Y + 1
    message_log = render_messages(world, width=MESSAGE_LOG_WIDTH, height=MESSAGE_LOG_HEIGHT)
    message_log.blit(dest=console, dest_x=MESSAGE_LOG_X, dest_y=message_log_y)
