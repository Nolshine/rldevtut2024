#!/usr/bin/env python3
import time
from random import Random

import tcod
import tcod.ecs
from typing import TYPE_CHECKING, Callable, Optional

from components.components import Graphic
import constants.colors as colors
from constants.game_constants import *
from constants.map_constants import *
from constants.tags import IsPlayer, ActiveMap
from engine.game_globals import *
from engine.actor_helpers import create_actor, update_fov
from engine.states import DefaultState
from dungeon.procgen import generate_caves
import mobs.entity_prefabs as prefabs



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
    player = create_actor((0, 0), prefabs.player, world)
    # player.tags.add(IsPlayer)

    map_ = generate_caves(
        world,
        SCREEN_W,
        SCREEN_H,
        ROOM_MAX_SIZE,
        ROOM_MIN_SIZE,
        MAX_ROOMS,
    )
    world[None].relation_tag[ActiveMap] = map_
    game_state = DefaultState(world)
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
                game_state.on_event(event)
                


if __name__ == "__main__":
    main()
