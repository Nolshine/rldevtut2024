from __future__ import annotations

from random import Random

import tcod.ecs

import constants.colors as colors
from constants.tags import IsPlayer, IsActor, IsCorpse
from components.main import AI, HP, HPMax, Defense, Graphic, Name, Power
from engine.messaging import add_message


def melee_damage(attacker: tcod.ecs.Entity, target: tcod.ecs.Entity) -> int:
    """Get melee damage for attacking `target`."""
    rng: Random = attacker.registry[None].components[Random]
    attacker_power = attacker.components.get(Power)
    assert attacker_power is not None
    target_defense = target.components.get(Defense)
    assert target_defense is not None
    pre_damage = rng.randint(attacker_power.min, attacker_power.max)
    return max(0, pre_damage - target_defense.value)

def apply_damage(entity: tcod.ecs.Entity, damage: int) -> None:
    """Deal damage to an entity."""
    assert entity.components[HP] is not None
    entity.components[HP].value -= damage
    if entity.components[HP].value <= 0:
        die(entity)

def heal(actor: tcod.ecs.Entity, heal_amt: int) -> int:
    """Heal an entity.."""
    assert actor.components.get(HP, None) is not None
    hp = actor.components[HP].value
    max_hp = actor.components[HPMax].value
    if hp == max_hp:
        return 0
    new_hp = min(hp + heal_amt, max_hp)
    healed = new_hp - hp
    actor.components[HP].value = new_hp
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
    entity.tags.add(IsCorpse)
