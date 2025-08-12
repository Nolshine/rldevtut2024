from dataclasses import dataclass

import constants.colors as colors
from components.main import Component, Graphic, HPMax, Power, Defense, Inventory
from constants.tags import IsActor, IsBlocking, IsPlayer


@dataclass
class MobPrefab:
    name: str
    graphic: Graphic
    tags: list[str]
    components: list[Component]

player = MobPrefab(
    name="Player",
    graphic=Graphic("@", colors.WHITE),
    tags=[IsPlayer, IsActor, IsBlocking],
    components=[
        HPMax(30),
        Power(min=3, max=5),
        Defense(2),
        Inventory(0, 26),
    ]
)
orc = MobPrefab(
    name="Orc",
    graphic=Graphic("o", colors.ORC),
    tags=[IsActor, IsBlocking],
    components=[
        HPMax(10),
        Power(min=2, max=4),
        Defense(0),
    ]
)
troll = MobPrefab(
    name="Troll",
    graphic=Graphic("T", colors.TROLL),
    tags=[IsActor, IsBlocking],
    components=[
        HPMax(16),
        Power(min=3,max=6),
        Defense(1),
    ]
)
