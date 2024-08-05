from __future__ import annotations

from typing import Final

import attrs

import constants.colors as colors



@attrs.define
class Message:
    """A single log message."""

    text: str
    fg_color: str
    count: int = 1

    
    @property
    def fg(self) -> tuple[int, int, int]:
        """Return the colour of the message text"""
        fg: tuple[int, int, int] = getattr(colors, self.fg_color)
        return fg
    
    @property
    def full_text(self) -> str:
        """The full text of this message, including the message count if necessary."""
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text
    
MessageLog: Final = list[Message]