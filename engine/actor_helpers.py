from typing import Tuple

import numpy as np
import tcod
import tcod.constants
import tcod.ecs
import tcod.map

from components.components import Graphic, Position
from components.components import Tiles, VisibleTiles, ExploredTiles
from constants.tags import InMap
from constants.game_constants import PLAYER_FOV_RADIUS
from dungeon.tiles import TILES, TileIndices

def create_actor(x: int, y: int, char: str, fg: Tuple[int, int, int], world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    entity = world[object()]
    entity.components[Position] = Position(x, y)
    entity.components[Graphic] = Graphic(char, fg)
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