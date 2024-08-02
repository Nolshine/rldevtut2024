from typing import Protocol, Optional, Callable

from tcod.console import Console
from tcod.event import Event
from tcod.ecs import Entity, Registry

from components.components import Name
from constants.tags import IsActor, IsPlayer, ActiveMap, InMap
from engine.input_handlers import DefaultHandler
from engine.render_helpers import render_all_entities, render_map
from actions.action_helpers import do_player_action



class State(Protocol):
    __slots__ = ()

    def on_event(self, event: Event) -> None:
        pass
    def on_draw(self, console: Console) -> None:
        pass



class DefaultState(State):
    def __init__(self, world: Registry) -> None:
        self.event_handler = DefaultHandler()
        self.world = world

    def on_event(self, event: Event) -> None:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        action: Optional[Callable[[Entity], None]] = self.event_handler.dispatch(event)

        if action is None:
            return
        do_player_action(player, action)
    
    def on_draw(self, console: Console) -> None:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        map_ = self.world[None].relation_tag[ActiveMap]
        render_map(console, map_)
        render_all_entities(console, self.world, player)