import tcod.ecs

from components.main import Graphic, Name, Healing
from constants.tags import IsItem, IsQuaffable
import constants.colors as colors



def register_items(world: tcod.ecs.Registry) -> None:
    # consumables
    item = world["health_potion"]
    item.components[Name] = "Health Potion"
    item.components[Graphic] = Graphic("!", colors.MAGENTA)
    item.components[Healing] = 10
    for tag in [IsItem, IsQuaffable]:
        item.tags.add(tag)
