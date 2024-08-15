#!/usr/bin/env python3
import time
import traceback
from random import Random

import tcod
import tcod.ecs

from mobs.mob_prefabs import player as player_prefab
from constants.game_constants import *
from constants.map_constants import *
from constants.tags import ActiveMap
from components.message_log import MessageLog
from engine.game_globals import *
from engine.actor_helpers import create_actor, update_fov
from engine.messaging import add_message
from engine.state import State
from engine.states import DefaultState
from dungeon.procgen import generate_caves



def main() -> None:
    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        FONT_PATH,
        FONT_COLS,
        FONT_ROWS,
        tcod.tileset.CHARMAP_CP437,
    )
    seed = int(time.time())
    print(f"Seed: {seed}")
    root_console = tcod.console.Console(SCREEN_W, SCREEN_H, order="F")

    world = tcod.ecs.Registry()
    rng = Random()
    rng.seed(seed)
    world[None].components["Random"] = rng
    player = create_actor((0, 0), player_prefab, world)

    map_ = generate_caves(
        world,
        MAP_WIDTH,
        MAP_HEIGHT,
        ROOM_MAX_SIZE,
        ROOM_MIN_SIZE,
        MAX_ROOMS,
    )
    world[None].relation_tag[ActiveMap] = map_

    game_state: State = DefaultState(world)

    world[None].components[MessageLog] = MessageLog()

    update_fov(player)

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
                try:
                    game_state = game_state.on_event(event)
                except Exception as err:
                    traceback.print_exc()
                    add_message(world, f"{str(err)}", "RED")



if __name__ == "__main__":
    main()
