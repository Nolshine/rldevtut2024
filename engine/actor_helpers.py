import numpy as np
import tcod
import tcod.constants
import tcod.ecs
import tcod.map

from components.main import Position
from components.main import Tiles, VisibleTiles, ExploredTiles
from constants.tags import InMap
from constants.game_constants import PLAYER_FOV_RADIUS
from dungeon.tiles import TILES

def update_fov(entity: tcod.ecs.Entity) -> None:
    map_: tcod.ecs.Entity = entity.relation_tag[InMap]
    transparency = TILES["transparent"][map_.components[Tiles]]
    map_.components[VisibleTiles] = visible = tcod.map.compute_fov(
        transparency=transparency,
        pov=entity.components[Position].packed,
        radius=PLAYER_FOV_RADIUS,
        algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST,
    )
    map_.components[ExploredTiles] = np.where(visible, map_.components[Tiles], map_.components[ExploredTiles])
