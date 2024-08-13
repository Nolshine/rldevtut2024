from __future__ import annotations

from typing import Final


# Identity/categorisation tags
IsPlayer: Final = "IsPlayer"
IsActor: Final = "IsActor"
IsBlocking: Final = "IsBlocking" # an entity that blocks movement
IsItem: Final = "IsItem"
IsQuaffable: Final = "IsQuaffable" # potions, draughts, cola, etc


# Association/relational tags
ActiveMap: Final = "ActiveMap"
InMap: Final = "InMap"
InInventory: Final = "InInventory" # for entities that are associtead with an actor's inventory