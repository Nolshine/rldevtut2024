from __future__ import annotations

from typing import Callable

import tcod.ecs

from engine.state import State
import engine.states as states
from engine.messaging import add_message
from actions.action import ActionResult, Success, Failure
from constants.tags import IsPlayer, IsActor, ActiveMap, InMap
from components.main import HP, AI


def do_player_action(state: State, player: tcod.ecs.Entity, action: Callable[[tcod.ecs.Entity], ActionResult]) -> State:
    assert IsPlayer in player.tags
    world = player.registry
    result: ActionResult = action(player)

    match result:
         case Success():
              do_enemy_actions(player.registry)
         case Failure(reason=reason):
              add_message(world, reason, "GREY")

    if player.components[HP].value <= 0:
         return states.GameOverState(world)
    return state

def do_enemy_actions(r: tcod.ecs.Registry):
        map_ = r[None].relation_tag[ActiveMap]
        npcs = r.Q.all_of(components=[AI], tags=[IsActor], relations=[(InMap, map_)]).none_of(tags=[IsPlayer])
        for entity in npcs:
            entity.components[AI].action(entity)
