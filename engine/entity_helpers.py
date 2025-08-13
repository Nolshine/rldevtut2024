import tcod.ecs

from components.main import Position
from constants.tags import InMap



def spawn(name: str, map_: tcod.ecs.Entity | None, x: int, y: int, world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    new_entity = world[name].instantiate()
    new_entity.components[Position] = Position(x, y)
    if map_ is not None:
        new_entity.relation_tag[InMap] = map_

    return new_entity
