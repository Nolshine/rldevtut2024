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