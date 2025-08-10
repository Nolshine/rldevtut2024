from __future__ import annotations

from tcod.context import SDL_WINDOW_FULLSCREEN
from tcod.tileset import CHARMAP_TCOD


# main font
FONT_PATH = "assets/solarmono32x8.png"
FONT_COLS = 32
FONT_ROWS = 8
TCOD_TILESET = CHARMAP_TCOD

# configuration
FLAGS = SDL_WINDOW_FULLSCREEN
WINDOW_TITLE = "Yet Another Roguelike Tutorial"
WINDOW_VSYNC = True
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# player tuning - player stats that can not change go here
PLAYER_FOV_RADIUS = 10

# behaviour tuning - things like how enemies will path
PATH_COST_INCREASE = 15
