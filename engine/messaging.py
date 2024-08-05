from __future__ import annotations

import tcod.ecs

import constants.colors as colors
from components.message_log import MessageLog, Message


def add_message(world: tcod.ecs.Registry, text: str, fg: str = "WHITE"):
    """Append a message to the message log, stacking if necessary."""
    assert hasattr(colors, fg), fg
    log: list[Message] = world[None].components[MessageLog]
    if log and log[-1] == text:
        log[-1].count += 1
        return
    log.append(Message(text, fg))