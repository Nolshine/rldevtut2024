#!/usr/bin/env python3
import tcod
import tcod.ecs
from typing import TYPE_CHECKING, Callable, Optional

import constants.colors as colors
from constants.game_constants import *
from engine.game_globals import *
from components.components import Position, Graphic
from constants.tags import IsPlayer
from engine.input_handlers import EventHandler



def main() -> None:
    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        FONT_PATH,
        FONT_COLS,
        FONT_ROWS,
        tcod.tileset.CHARMAP_CP437,
    )
    root_console = tcod.console.Console(SCREEN_W, SCREEN_H, order="F")

    world = tcod.ecs.Registry()
    player = world[object()]
    player.components[Position] = Position(int(SCREEN_W/2), int(SCREEN_H/2))
    player.components[Graphic] = Graphic("@", colors.WHITE)
    player.tags.add(IsPlayer)

    npc = world[object()]
    npc.components[Position] = Position(player.components[Position].x + 2, player.components[Position].y)
    npc.components[Graphic] = Graphic("?", colors.YELLOW)
    
    event_handler = EventHandler()

    with tcod.context.new_terminal(
        SCREEN_W,
        SCREEN_H,
        tileset=tileset,
        title=WINDOW_TITLE,
        vsync=WINDOW_VSYNC,
        sdl_window_flags=FLAGS,
    ) as context:

        while True:
            root_console.clear()
            for entity in world.Q.all_of(components=[Position, Graphic]):
                if IsPlayer in entity.tags:
                    continue
                pos = entity.components[Position]
                if not (0 <= pos.x < root_console.width and 0 <= pos.y < root_console.height):
                    continue
                graphic = entity.components[Graphic]
                root_console.print(pos.x, pos.y, graphic.char, graphic.fg)
            pos = player.components[Position]
            graphic = player.components[Graphic]
            root_console.print(pos.x, pos.y, graphic.char, graphic.fg)
            context.present(root_console)

            for event in tcod.event.wait():
                action: Optional[Callable[[tcod.ecs.Entity], None]] = event_handler.dispatch(event)

                if action is None:
                    continue
                action(player)
                


if __name__ == "__main__":
    main()
