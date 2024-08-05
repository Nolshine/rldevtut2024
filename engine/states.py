from typing import Protocol, Optional, Callable

import tcod.event
from tcod.console import Console
from tcod.ecs import Entity, Registry
from tcod.event import KeySym


import constants.colors as colors
from constants.tags import IsPlayer
from constants.controls import MOVEMENT_KEYS, WAIT_KEYS
from constants.gui_constants import HEALTH_BAR_WIDTH
from components.components import HP, HPMax
from engine.render_helpers import render_all_entities, render_map, render_bar
from actions.actions import Bump, escape_action, regenenerate_map, reveal_map, wait_action
from actions.action_helpers import do_player_action
from engine.state import State



class BaseState(State):
    """Implements common initializer"""
    def __init__(self, world: Registry):
        self.world = world

class DefaultState(BaseState):
    """The default mode, wherein the player is exploring the dungeon."""
    def on_event(self, event: tcod.event.Event) -> State:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in MOVEMENT_KEYS:
                return do_player_action(self, player, Bump(*MOVEMENT_KEYS[sym]))
            case tcod.event.KeyDown(sym=sym) if sym in WAIT_KEYS:
                return do_player_action(self, player, wait_action)
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return do_player_action(self, player, escape_action)
            case tcod.event.KeyDown(sym=KeySym.F1):
                regenenerate_map(player)
            case tcod.event.KeyDown(sym=KeySym.F2):
                reveal_map(player)
        return self
    
    def on_draw(self, console: Console) -> None:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        render_map(console, self.world)
        render_all_entities(console, self.world)
        render_bar(console, player.components[HP], player.components[HPMax], HEALTH_BAR_WIDTH)

class GameOverState(BaseState):
    """The player has died - they cannot move and must restart or load a save."""
    def on_event(self, event: tcod.event.Event) -> State:
        if event.type == "KEYDOWN" and event.sym == KeySym.ESCAPE:
            raise SystemExit()
        return self
        
    def on_draw(self, console: Console) -> None:
        (player,) = self.world.Q.all_of(tags=[IsPlayer])
        render_map(console, self.world)
        render_all_entities(console, self.world)
        render_bar(console, player.components[HP], player.components[HPMax], HEALTH_BAR_WIDTH)
        
        frame_width = len("GAME OVER") + 2
        frame_height = 5
        frame_x = (console.width // 2) - frame_width // 2
        frame_y = (console.height // 2) - 2
        console.draw_frame(
            x=frame_x,
            y=frame_y,
            width=frame_width,
            height=frame_height,
            title="Oh No",
            fg=colors.WHITE,
            bg=colors.BLACK,
        )
        console.print(frame_x + 1, frame_y + 2, "YOU DIED!", fg=colors.RED)