#!/usr/bin/env python3
import tcod
import tcod.ecs
from typing import TYPE_CHECKING, Callable, Optional

import constants.colors as colors
from constants.game_constants import *
from constants.tags import IsPlayer
from engine.game_globals import *
from engine.helpers import create_actor
from engine.states import DefaultState



def main() -> None:
    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        FONT_PATH,
        FONT_COLS,
        FONT_ROWS,
        tcod.tileset.CHARMAP_CP437,
    )
    root_console = tcod.console.Console(SCREEN_W, SCREEN_H, order="F")

    world = tcod.ecs.Registry()
    player = create_actor(int(SCREEN_W/2), int(SCREEN_H/2), "@", colors.WHITE, world)
    player.tags.add(IsPlayer)
    npc = create_actor(int(SCREEN_W/2) + 2, int(SCREEN_H/2), "?", colors.YELLOW, world)

    game_state = DefaultState(world)

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
            game_state.on_draw(root_console)
            context.present(root_console)

            for event in tcod.event.wait():
                game_state.on_event(event)
                


if __name__ == "__main__":
    main()
