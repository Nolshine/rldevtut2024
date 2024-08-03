from __future__ import annotations

from tcod.context import SDL_WINDOW_FULLSCREEN_DESKTOP



# main font
FONT_PATH = "assets/terminal16x16_gs_ro.png"
FONT_COLS = 16
FONT_ROWS = 16

# configuration
FLAGS = None #SDL_WINDOW_FULLSCREEN_DESKTOP
WINDOW_TITLE = "Yet Another Roguelike Tutorial"
WINDOW_VSYNC = True
SCREEN_W = 80
SCREEN_H = 50

# player tuning - player stats that can not change go here
PLAYER_FOV_RADIUS = 10

# behaviour tuning - things like how enemies will path
PATH_COST_INCREASE = 15