from __future__ import annotations

import time
from typing import Final

import numpy as np
import tcod.ecs

from actions.action import Success, Failure, ActionResult
from constants.game_constants import SCREEN_W, SCREEN_H
from constants.map_constants import *
from constants.tags import ActiveMap, IsActor, IsBlocking, IsPlayer, InMap
from components.components import Name, Position, Tiles, VisibleTiles, ExploredTiles
from dungeon.tiles import TILES
from engine.actor_helpers import update_fov
from engine.path_tools import path_to
from mobs.combat import melee_damage, apply_damage

class Move:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        r = entity.registry
        map_ = entity.relation_tag[InMap]
        map_tiles = entity.registry[None].relation_tag[ActiveMap].components[Tiles]
        pos = entity.components[Position]
        target = Position(pos.x + self.dx, pos.y + self.dy)
        if TILES[map_tiles[target.x, target.y]]["walk_cost"] == 0:
            return Failure("WARNING: Move action attempted into unwalkable tile.")
        blocking = r.Q.all_of(tags=[IsActor, IsBlocking, target], relations=[(InMap, map_)]).get_entities()
        if len(blocking) > 0:
            return Failure("Something is blocking the way.")
        entity.components[Position] = target
        if IsPlayer in entity.tags:
            update_fov(entity)
        return Success()

class Melee:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        new_pos = entity.components[Position] + (self.dx, self.dy)
        attacker_is_player = IsPlayer in entity.tags
        try:
            (target,) = entity.registry.Q.all_of(tags=[IsActor, new_pos])
        except ValueError:
            return Failure("Nothing there to attack.")
        defender_is_player = IsPlayer in entity.tags
        dmg = melee_damage(entity, target)
        attack_desc: str
        if attacker_is_player:
            attack_desc = f"You hit the {target.components[Name]} for {dmg} HP!"
        elif defender_is_player:
            attack_desc = f"The {entity.components[Name]} hits you for {dmg} HP!"
        else:
            attack_desc = f"The {entity.components[Name]} hits the {target.components[Name]} for {dmg} HP!"
        print(attack_desc)
        apply_damage(target, dmg)
        return Success()

class Bump:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy
    
    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        map_ = entity.relation_tag[InMap]
        r = entity.registry
        pos = entity.components[Position]
        target = Position(pos.x + self.dx, pos.y + self.dy)
        map_tiles = r[None].relation_tag[ActiveMap].components[Tiles]
        if TILES[map_tiles[target.x, target.y]]["walk_cost"] == 0:
            return Failure("You cannot move there.")
        entities = r.Q.all_of(tags=[IsActor, IsBlocking, target], relations=[(InMap, map_)]).get_entities()
        if len(entities) > 0:
            return Melee(self.dx, self.dy)(entity)
        else:
            return Move(self.dx, self.dy)(entity)
        
class SimpleEnemy:
    def __init__(self) -> None:
        self.path: list[Position] = []

    def __call__(self, actor: tcod.ecs.Entity):
        (target,) = actor.registry.Q.all_of(tags=[IsPlayer])
        actor_pos: Final = actor.components[Position]
        target_pos: Final = target.components[Position]
        map_: Final = actor.relation_tag[InMap]
        if not (map_ == target.relation_tag[InMap]):
            # don't path to the player if it's not in the same map
            # this shouldn't occur, so we want to know if it does
            print("WARNING: Actor tried pathing from different map")
            return wait_action(actor)
        dx: Final = target_pos.x - actor_pos.x
        dy: Final = target_pos.y - actor_pos.y
        distance: Final = max(abs(dx), abs(dy)) # Chebyshev distance
        if map_.components[VisibleTiles][actor_pos.raw]:
            if distance <= 1:
                return Melee(dx, dy)(actor)
            self.path = path_to(actor, target_pos)
        if self.path:
            dest: Final = self.path.pop(0)
            return Move(dest.x - actor_pos.x, dest.y - actor_pos.y)(actor)
        return wait_action(actor)


def escape_action(entity: tcod.ecs.Entity) -> ActionResult:
    raise SystemExit()
    return Success()

def regenenerate_map(entity: tcod.ecs.Entity) -> ActionResult: # TODO: remove when not in testing builds
    r = entity.registry
    new_seed = int(time.time())
    print(f"Seed: {new_seed}")
    r[None].components["Random"].seed(new_seed)
    map(lambda e : e.clear(), r.Q.all_of(relations=[(InMap, ...)]).none_of(tags=[IsPlayer]))
    r[None].relation_tag[ActiveMap].clear()
    map_ = generate_caves(
        r,
        SCREEN_W,
        SCREEN_H,
        ROOM_MAX_SIZE,
        ROOM_MIN_SIZE,
        MAX_ROOMS,
    )
    r[None].relation_tag[ActiveMap] = map_
    update_fov(entity)
    return Failure("DEBUG ACTION: regenerate map")

def reveal_map(entity: tcod.ecs.Entity) -> ActionResult:
    r = entity.registry
    map_ = entity.relation_tag[InMap]
    map_.components[ExploredTiles] = np.copy(map_.components[Tiles])
    return Failure("DEBUG ACTION: reveal map")

def wait_action(entity: tcod.ecs.Entity) -> ActionResult:
    # do nothing for one turn
    return Success()

from dungeon.procgen import generate_caves