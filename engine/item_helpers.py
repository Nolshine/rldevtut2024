import tcod.ecs

from components.main import Name, Position, Graphic
from items.item_prefabs import ItemPrefab



def create_item(pos: tuple[int, int], prefab: ItemPrefab, world: tcod.ecs.Registry) -> tcod.ecs.Entity:
    item = world[object()]
    item.components[Name] = prefab.name
    item.components[Position] = Position(pos[0], pos[1])
    item.components[Graphic] = prefab.graphic
    for tag in prefab.tags:
        item.tags.add(tag)
    for component in prefab.components:
        item.components[type(component)] = component

    return item
