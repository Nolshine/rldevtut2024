import tcod.ecs

import constants.colors as colors
from components.main import Name, Graphic, HPMax, HP, Power, Defense, Inventory, AI
from constants.tags import IsActor, IsBlocking


def register_mobs(world: tcod.ecs.Registry) -> None:
    actor = world["player"]
    actor.components[Name] = "Player"
    actor.components[Graphic] = Graphic("@", colors.WHITE)
    actor.components[HPMax] = 30
    actor.components[HP] = 30
    actor.components[Power] = Power(min=3, max=5)
    actor.components[Defense] = 2
    actor.components[Inventory] = Inventory.from_size(26)
    for tag in [IsActor, IsBlocking]:
        actor.tags.add(tag)

    actor = world["orc"]
    actor.components[Name] = "Orc"
    actor.components[Graphic] = Graphic("o", colors.ORC)
    actor.components[HPMax] = 10
    actor.components[HP] = 10
    actor.components[Power] = Power(min=2, max=4)
    actor.components[Defense] = 0
    for tag in [IsActor, IsBlocking]:
        actor.tags.add(tag)

    actor = world["troll"]
    actor.components[Name] = "Troll"
    actor.components[Graphic] = Graphic("T", colors.TROLL)
    actor.components[HPMax] = 16
    actor.components[HP] = 16
    actor.components[Power] = Power(min=3, max=6)
    actor.components[Defense] = 1
    for tag in [IsActor, IsBlocking]:
        actor.tags.add(tag)
