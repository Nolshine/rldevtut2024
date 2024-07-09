from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction



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

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None # This will be returned if no valid key is presed

        key = event.sym

        if key in movement_keys:
            action = MovementAction(*movement_keys[key])
        
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action