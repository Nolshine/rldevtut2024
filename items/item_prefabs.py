import attrs

from components.main import Graphic
from constants.tags import IsItem, IsQuaffable
import constants.colors as colors



@attrs.define(frozen=True)
class ItemPrefab:
    name: str
    graphic: Graphic
    tags: list[str]
    healing: int | None

health_potion = ItemPrefab(
    name="Health Potion",
    graphic=Graphic("!", colors.MAGENTA),
    tags=[IsItem, IsQuaffable],
    healing=10,
)
