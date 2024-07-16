from tcod.context import SDL_WINDOW_FULLSCREEN_DESKTOP
# deviating from tutorial to organise code/references

# main font
FONT_PATH: str = "terminal16x16_gs_ro.png"
FONT_COLS: int = 16
FONT_ROWS:int  = 16

# configuration
FLAGS: int = SDL_WINDOW_FULLSCREEN_DESKTOP
WINDOW_TITLE: str = "Yet Another Roguelike Tutorial"
WINDOW_VSYNC: bool = True
SCREEN_W: int = 80
SCREEN_H: int = 50
