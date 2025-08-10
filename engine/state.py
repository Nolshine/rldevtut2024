from typing import Protocol

from tcod.event import Event
from tcod.console import Console

class State(Protocol):
    __slots__ = ()

    def on_event(self, event: Event) -> "State":
        ...
    def on_draw(self, console: Console) -> None:
        ...
