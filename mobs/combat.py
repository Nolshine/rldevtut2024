from __future__ import annotations

from random import Random

import tcod.ecs

from constants.tags import IsPlayer, IsActor
from components.main import AI, HP, Defense, Graphic, Name, PowerMin, PowerMax
import constants.colors as colors



def melee_damage(entity: tcod.ecs.Entity, target: tcod.ecs.Entity) -> int:
    """Get melee damage for attacking `target`."""
    rng: Random = entity.registry[None].components["Random"]
    pre_damage = rng.randint(entity.components.get(PowerMin, 0), entity.components.get(PowerMax, 0))
    return max(0, pre_damage - target.components.get(Defense, 0))

def apply_damage(entity: tcod.ecs.Entity, damage: int) -> None:
    """Deal damage to an entity."""
    entity.components[HP] -= damage
    if entity.components[HP] <= 0:
        die(entity)

def die(entity: tcod.ecs.Entity) -> None:
    """Kill an entity."""
    is_player = IsPlayer in entity.tags
    # TODO add a message to ingame log
    print("You died!" if is_player else f"{entity.components[Name]} has died!")
    entity.components[Graphic] = Graphic("%", colors.DARK_RED)
    entity.components[Name] = f"remains of {entity.components[Name]}"
    if not is_player:
        entity.components.pop(AI)
    entity.tags.remove(IsActor)
