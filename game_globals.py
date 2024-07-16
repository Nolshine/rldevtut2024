from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import SDL_WINDOW_FULLSCREEN_DESKTOP

if TYPE_CHECKING:
    import tcod.context
    import tcod.console
    import tcod.ecs

    from input_handlers import EventHandler
# deviating from tutorial to organise code/references


#--- immutables ---#
# main font
FONT_PATH = "terminal16x16_gs_ro.png"
FONT_COLS = 16
FONT_ROWS = 16

# configuration
FLAGS = SDL_WINDOW_FULLSCREEN_DESKTOP
WINDOW_TITLE = "Yet Another Roguelike Tutorial"
WINDOW_VSYNC = True
SCREEN_W = 80
SCREEN_H = 50


#--- mutables ---#
context: tcod.context.Context
root_console: tcod.console.Console
event_handler: EventHandler
world: tcod.ecs.Registry