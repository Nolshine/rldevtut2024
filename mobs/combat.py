from __future__ import annotations

from random import Random

import tcod.ecs

import constants.colors as colors
from constants.tags import IsPlayer, IsActor
from components.main import AI, HP, HPMax, Defense, Graphic, Name, PowerMin, PowerMax
from engine.messaging import add_message


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

def heal(actor: tcod.ecs.Entity, heal_amt: int) -> int:
    """Heal an entity.."""
    assert actor.components.get(HP, None) is not None
    hp = actor.components[HP]
    max_hp = actor.components[HPMax]
    if hp == max_hp:
        return 0
    new_hp = min(hp + heal_amt, max_hp)
    healed = new_hp - hp
    actor.components[HP] = new_hp
    return healed
        

def die(entity: tcod.ecs.Entity) -> None:
    """Kill an entity."""
    is_player = IsPlayer in entity.tags
    death_str = "You died!" if is_player else f"{entity.components[Name]} has died!"
    color_str = "PLAYER_DIE" if is_player else "ENEMY_DIE"
    add_message(entity.registry, death_str, color_str)
    entity.components[Graphic] = Graphic("%", colors.DARK_RED)
    entity.components[Name] = f"remains of {entity.components[Name]}"
    if not is_player:
        entity.components.pop(AI)
    entity.tags.remove(IsActor)
