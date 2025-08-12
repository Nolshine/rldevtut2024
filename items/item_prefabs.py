import attrs

from components.main import Graphic, Component, Healing
from constants.tags import IsItem, IsQuaffable
import constants.colors as colors



@attrs.define(frozen=True)
class ItemPrefab:
    name: str
    graphic: Graphic
    tags: list[str]
    components: list[Component]

small_healing_potion = ItemPrefab(
    name="Health Potion (s)",
    graphic=Graphic("!", colors.MAGENTA),
    tags=[IsItem, IsQuaffable],
    components=[
        Healing(amount=10),
    ]
)
