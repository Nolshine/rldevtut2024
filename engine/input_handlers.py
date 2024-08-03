import tcod.event
import tcod.ecs

from actions.action import Action
from actions.actions import Bump, escape_action, regenenerate_map, reveal_map



movement_keys = {
    # cursors keys
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),

    # numpad keys
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_4: (-1, 0),
    # tcod.event.KeySym.KP_5: (0, 0), # pass turn key
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
}

class DefaultHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Action | None = None # This will be returned if no valid key is presed

        key = event.sym

        if key in movement_keys:
            action = Bump(*movement_keys[key])
        
        elif key == tcod.event.KeySym.ESCAPE:
            action = escape_action

        elif key == tcod.event.KeySym.F1: # TODO: Remove when finished with testing builds
            action = regenenerate_map
        elif key == tcod.event.KeySym.F2:
            action = reveal_map

        return action