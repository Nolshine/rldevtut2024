import tcod.ecs

from components.main import HP, HPMax
from components.item_effects import Healing



def heal(actor: tcod.ecs.Entity, heal_amt: int) -> int:
    """Attempt to heal an actor by an amount.
    Returns the actual amount of healing done."""
    assert actor.components[HP]
    max_hp = actor.components[HPMax]
    cur_hp = actor.components[HP]
    if cur_hp == max_hp:
        return 0
    new_hp = cur_hp + heal_amt
    if new_hp > max_hp:
        new_hp = max_hp
    healed = new_hp - cur_hp
    actor.components[HP] = new_hp
    return healed

table = {
    Healing: heal,
}
