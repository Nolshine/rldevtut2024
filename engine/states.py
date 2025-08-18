from typing import Callable, Self

import attrs
import tcod.event
from tcod.console import Console
from tcod.ecs import Entity, Registry
from tcod.event import KeySym


import constants.colors as colors
from constants.tags import IsPlayer, IsItem, InInventory, IsQuaffable
from constants.controls import MOVEMENT_KEYS, WAIT_KEYS, SELECT_KEYS
from constants.gui_constants import ITEM_SELECT_FRAME_WIDTH, ITEM_SELECT_FRAME_HEIGHT
from components.main import Name, HP, HPMax, Inventory
from engine.render_helpers import render_main
from engine.item_helpers import create_item
from items.item_prefabs import small_healing_potion
from actions.action import Action
from actions.actions import Bump, GetItem, DropItem, QuaffItem, escape_action, regenenerate_map, reveal_map, wait_action
from engine.state import State
from actions.action_helpers import do_player_action


@attrs.define
class BaseState(State):
    """Implements common initializer"""
    world: Registry

@attrs.define
class DefaultState(BaseState):
    """The default mode, wherein the player is exploring the dungeon."""
    def on_event(self, event: tcod.event.Event) -> State:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in MOVEMENT_KEYS:
                return do_player_action(self, player, Bump(*MOVEMENT_KEYS[sym]))
            case tcod.event.KeyDown(sym=sym) if sym in WAIT_KEYS:
                return do_player_action(self, player, wait_action)
            case tcod.event.KeyDown(sym=KeySym.G):
                return do_player_action(self, player, GetItem())
            case tcod.event.KeyDown(sym=KeySym.D):
                return SelectItem.player_verb(player, "drop", DropItem, [IsItem])
            case tcod.event.KeyDown(sym=KeySym.Q):
                return SelectItem.player_verb(player, "quaff", QuaffItem, [IsItem, IsQuaffable])
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return do_player_action(self, player, escape_action)
            # TODO: The following are debug keys. remove in release versions.
            case tcod.event.KeyDown(sym=KeySym.F1):
                regenenerate_map(player)
            case tcod.event.KeyDown(sym=KeySym.F2):
                reveal_map(player)
            case tcod.event.KeyDown(sym=KeySym.F3):
                # full heal player
                player.components[HP].value = player.components[HPMax].value
            case tcod.event.KeyDown(sym=KeySym.F4):
                # fill player inventory with health potions
                for item in self.world.Q.all_of(tags=[IsItem], relations=[(InInventory, player)]):
                    item.clear()
                for i in range(26): # type: ignore
                    item = create_item((0, 0), small_healing_potion, self.world)
                    item.relation_tag[InInventory] = player
                player.components[Inventory].size = 26
            case _:
                pass
        return self

    def on_draw(self, console: Console) -> None:
        render_main(console, self.world)

@attrs.define
class GameOverState(BaseState):
    """The player has died - they cannot move and must restart or load a save."""
    def on_event(self, event: tcod.event.Event) -> State:
        match event:
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                raise SystemExit
            case _:
                pass
        return self

    def on_draw(self, console: Console) -> None:
        render_main(console, self.world)

        frame_width = len("GAME OVER") + 2
        frame_height = 5
        frame_x = (console.width // 2) - frame_width // 2
        title_x = frame_x + 1
        frame_y = (console.height // 2) - 2
        console.draw_frame(
            x=frame_x,
            y=frame_y,
            width=frame_width,
            height=frame_height,
            fg=colors.WHITE,
            bg=colors.BLACK,
        )
        console.print(x=title_x, y=frame_y, text="Oh no!", fg=colors.WHITE)
        console.print(frame_x + 1, frame_y + 2, "YOU DIED!", fg=colors.RED)

@attrs.define(kw_only=True)
class SelectItem(BaseState):
    items: list[Entity]
    world: Registry
    on_select: Callable[[Entity], State]
    on_cancel: Callable[[Registry], State] | None = None
    title: str = "Select an item:"

    @classmethod
    def player_verb(cls, player: Entity, verb: str, action: Callable[[Entity], Action], tags: list[str]) -> Self:
        r = player.registry
        items = list(r.Q.all_of(tags=tags, relations=[(InInventory, player)]).get_entities())
        return cls(
            items=items,
            title=f"Select an item to {verb}:",
            world=r,
            on_select=lambda item: do_player_action(DefaultState(r), player, action(item)),
            on_cancel=DefaultState
        )

    def on_event(self, event: tcod.event.Event) -> State:
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in {ord(c) for c in SELECT_KEYS}:
                index = SELECT_KEYS.index(chr(sym))
                if index < len(self.items):
                    return self.on_select(self.items[index])
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                if self.on_cancel is not None:
                    return self.on_cancel(self.world)
            case _:
                pass
        return self

    def on_draw(self, console: Console) -> None:
        render_main(console, self.world)

        frame_w = ITEM_SELECT_FRAME_WIDTH
        frame_h = ITEM_SELECT_FRAME_HEIGHT
        frame_x = console.width // 2 - frame_w // 2
        frame_y = console.height // 2 - frame_h // 2
        console.draw_frame(
            x=frame_x,
            y=frame_y,
            width=frame_w,
            height=frame_h,
            fg=colors.WHITE,
            bg=colors.BLACK,
        )
        console.print(
            x=frame_x + 1,
            y=frame_y + 1,
            text=self.title,
            fg=colors.WHITE
        )
        for i, (item, key_chr) in enumerate(zip(self.items, SELECT_KEYS)):
            y = 3 + (i % 13)
            x = 2 + (i // 13) * (ITEM_SELECT_FRAME_WIDTH // 2)
            console.print(frame_x + x, frame_y + y, f"({key_chr}) {item.components.get(Name, "????")}")
