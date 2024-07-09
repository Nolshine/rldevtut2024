#!/usr/bin/env python3
import tcod
from typing import TYPE_CHECKING, Optional

from game_globals import *
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

if TYPE_CHECKING:
    from actions import Action

def main() -> None:

    player_x: int = int(SCREEN_W / 2)
    player_y: int = int(SCREEN_H / 2)

    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        FONT_PATH,
        FONT_COLS,
        FONT_ROWS,
        tcod.tileset.CHARMAP_TCOD,
    )

    event_handler: EventHandler = EventHandler()

    with tcod.context.new_terminal(
        SCREEN_W,
        SCREEN_H,
        tileset=tileset,
        title=WINDOW_TITLE,
        vsync=WINDOW_VSYNC,
    ) as context:
        
        root_console: tcod.console.Console = tcod.console.Console(SCREEN_W, SCREEN_H, order="F")

        while True:
            root_console.print(player_x, player_y, string="@")
            
            context.present(root_console)
            root_console.clear()

            for event in tcod.event.wait():
                action: Optional[Action] = event_handler.dispatch(event)

                if action is None:
                    continue
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                
                elif isinstance(action, EscapeAction):
                    raise SystemExit()
                


if __name__ == "__main__":
    main()