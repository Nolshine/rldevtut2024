import tcod.ecs

from components.main import Name, Position, Graphic
from components.item_effects import Healing
from items.item_prefabs import ItemPrefab



def create_item(pos: tuple[int, int], prefab: ItemPrefab, world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    entity = world[object()]
    entity.components[Name] = prefab.name
    entity.components[Position] = Position(pos[0], pos[1])
    entity.components[Graphic] = prefab.graphic
    for tag in prefab.tags:
        entity.tags.add(tag)
    if prefab.healing:
        entity.components[Healing] = prefab.healing

    return entity
