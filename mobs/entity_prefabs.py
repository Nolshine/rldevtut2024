from dataclasses import dataclass
from typing import Final

import constants.colors as colors
from components.main import Graphic
from constants.tags import IsActor, IsBlocking, IsPlayer


@dataclass
class EntityPrefab:
    name: str
    graphic: Graphic
    hp_max: int | None
    power_min: int | None
    power_max: int | None
    defense: int | None
    tags: list[str]

player = EntityPrefab(
    name="Player",
    graphic=Graphic("@", colors.WHITE),
    hp_max=30,
    power_min=3,
    power_max=5,
    defense=2,
    tags=[IsPlayer, IsActor, IsBlocking]
)
orc = EntityPrefab(
    name="Orc",
    graphic=Graphic("o", colors.ORC),
    hp_max=10,
    power_min=2,
    power_max=4,
    defense=0,
    tags=[IsActor, IsBlocking]
)
troll = EntityPrefab(
    name="Troll",
    graphic=Graphic("T", colors.TROLL),
    hp_max=16,
    power_min=3,
    power_max=6,
    defense=1,
    tags=[IsActor, IsBlocking]
)