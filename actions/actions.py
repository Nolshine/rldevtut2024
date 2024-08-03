from __future__ import annotations

import time

import numpy as np
import tcod.ecs

from actions.action import Success, Failure, ActionResult
from constants.game_constants import SCREEN_W, SCREEN_H
from constants.map_constants import *
from constants.tags import ActiveMap, IsActor, IsBlocking, IsPlayer, InMap
from components.components import Name, Position, Tiles, ExploredTiles
from dungeon.procgen import generate_caves
from dungeon.tiles import TILES
from engine.actor_helpers import update_fov

class Move:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        map_tiles = entity.registry[None].relation_tag[ActiveMap].components[Tiles]
        pos = entity.components[Position]
        target = Position(pos.x + self.dx, pos.y + self.dy)
        if TILES[map_tiles[target.x, target.y]]["walk_cost"] == 0:
            return Failure("WARNING: Move action attempted into unwalkable tile.")
        entity.components[Position] = target
        if IsPlayer in entity.tags:
            update_fov(entity)
        return Success()

class Melee:
    def __init__(self, dx: int, dy: int, target: tcod.ecs.Entity):
        self.dx = dx
        self.dy = dy
        self.target = target

    def __call__(self, entity: tcod.ecs.Entity) -> ActionResult:
        prefix: str
        if IsPlayer in entity.tags:
            prefix = "You kick"
        else:
            prefix = f"The {entity.components[Name]} kicks"
        attack_str: str = f"{prefix} the {self.target.components[Name]}. They're not amused."
        print(attack_str)
        return Success()

class Bump:
    def __init__(self, dx: int, dy: int):
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
            return Melee(self.dx, self.dy, list(entities)[0])(entity)
        else:
            return Move(self.dx, self.dy)(entity)

def escape_action(entity: tcod.ecs.Entity) -> None:
    raise SystemExit()

def regenenerate_map(entity: tcod.ecs.Entity) -> None: # TODO: remove when not in testing builds
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

def reveal_map(entity: tcod.ecs.Entity) -> None:
    r = entity.registry
    map_ = entity.relation_tag[InMap]
    map_.components[ExploredTiles] = np.copy(map_.components[Tiles])