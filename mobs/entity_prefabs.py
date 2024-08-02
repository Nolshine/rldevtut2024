from dataclasses import dataclass
from typing import Final

import constants.colors as colors
from components.components import Graphic
from constants.tags import IsActor, IsBlocking, IsPlayer


@dataclass
class EntityPrefab:
    name: str
    graphic: Graphic
    tags: list[str]

player = EntityPrefab("Player", Graphic("@", colors.WHITE), [IsActor, IsBlocking, IsPlayer])
orc = EntityPrefab("Orc", Graphic("o", colors.ORC), [IsActor, IsBlocking])
troll = EntityPrefab("Troll", Graphic("T", colors.TROLL), [IsActor, IsBlocking])