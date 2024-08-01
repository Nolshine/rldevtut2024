from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tcod.context
    import tcod.console
    import tcod.ecs

    from engine.states import State



context: tcod.context.Context
root_console: tcod.console.Console
game_state: State
world: tcod.ecs.Registry


# For posterity: I was going to have these objects live here and not
# get passed around as parameters but I forgot somewhere along the way
# and the project is not structured to use this. These will remain here
# just to keep main.py clean, but otherwise this file is a little useless.
# Sorry if you cloned this repo and this file caused confusion!