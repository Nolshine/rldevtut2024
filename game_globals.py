from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tcod.context
    import tcod.console
    import tcod.ecs

    from input_handlers import EventHandler



context: tcod.context.Context
root_console: tcod.console.Console
event_handler: EventHandler
world: tcod.ecs.Registry