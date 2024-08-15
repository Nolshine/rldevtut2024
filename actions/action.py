from __future__ import annotations

from typing import Protocol, TypeAlias

import attrs
import tcod.ecs

@attrs.define
class Success:
    """Action has a successful result."""


@attrs.define
class Failure:
    """Action was not successful."""

    reason: str # What has failed?


ActionResult: TypeAlias = Success | Failure


class Action(Protocol):
    """Action protocol."""

    def __call__(self, actor: tcod.ecs.Entity, /) -> ActionResult:
        """Perform action"""
