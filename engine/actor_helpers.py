from typing import Tuple

import numpy as np
import tcod
import tcod.constants
import tcod.ecs
import tcod.ecs.entity
import tcod.map

from components.main import Graphic, Position, Name, HP, HPMax, PowerMin, PowerMax, Defense
from components.main import Tiles, VisibleTiles, ExploredTiles
from constants.tags import InMap, IsActor
from constants.game_constants import PLAYER_FOV_RADIUS
from dungeon.tiles import TILES
from mobs.entity_prefabs import EntityPrefab

def create_actor(pos: tuple[int, int], prefab: EntityPrefab, world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    entity = world[object()]
    entity.components[Name] = prefab.name
    entity.components[Position] = Position(pos[0], pos[1])
    entity.components[Graphic] = prefab.graphic
    entity.tags.add(IsActor)
    for tag in prefab.tags:
        entity.tags.add(tag)
    if prefab.hp_max:
        entity.components[HPMax] = prefab.hp_max
        entity.components[HP] = prefab.hp_max
    if prefab.power_min:
        entity.components[PowerMin] = prefab.power_min
    if prefab.power_max:
        entity.components[PowerMax] = prefab.power_max
    if prefab.defense:
        entity.components[Defense] = prefab.defense
    return entity

def update_fov(entity: tcod.ecs.Entity) -> None:
    map_: tcod.ecs.Entity = entity.relation_tag[InMap]
    transparency = TILES["transparent"][map_.components[Tiles]]
    map_.components[VisibleTiles] = visible = tcod.map.compute_fov(
        transparency=transparency,
        pov=entity.components[Position].raw,
        radius=PLAYER_FOV_RADIUS,
        algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST,
    )
    map_.components[ExploredTiles] = np.where(visible, map_.components[Tiles], map_.components[ExploredTiles])