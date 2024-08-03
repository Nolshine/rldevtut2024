from __future__ import annotations

from typing import Callable

import tcod.ecs

from actions.action import Success, ActionResult
from constants.tags import IsPlayer, IsActor, ActiveMap, InMap
from components.components import Name
from engine.actor_helpers import update_fov


def do_player_action(player: tcod.ecs.Entity, action: Callable[[tcod.ecs.Entity], None]):
    assert IsPlayer in player.tags
    result: ActionResult = action(player)
    if isinstance(result, Success):
         do_enemy_actions(player.registry)
    else:
         print(result.reason)

def do_enemy_actions(r: tcod.ecs.Registry):
        map_ = r[None].relation_tag[ActiveMap]
        npcs = r.Q.all_of(tags=[IsActor], relations=[(InMap, map_)]).none_of(tags=[IsPlayer])
        for entity in npcs:
            print(f"The {entity.components[Name]} wonders when it can have a go.")