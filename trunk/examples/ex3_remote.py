#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pyatspi

from cwiid import BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT, BTN_A, BTN_B, BTN_1, BTN_2, \
    BTN_MINUS, BTN_PLUS, BTN_HOME, Z, X, Y

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))
from wiimote import WiiMote


KEYCODE_Z = 52
KEYCODE_S = 39
KEYCODE_X = 53
KEYCODE_D = 40
KEYCODE_C = 54
KEYCODE_V = 55
KEYCODE_G = 42
KEYCODE_F = 41
KEYCODE_B = 56
KEYCODE_H = 43
KEYCODE_N = 57
KEYCODE_J = 44
KEYCODE_K = 45
KEYCODE_M = 58
KEYCODE_Q = 24
KEYCODE_P = 33
KEYCODE_UP = 111
KEYCODE_DOWN = 116
KEYCODE_LEFT = 113
KEYCODE_RIGTH = 114
KEYCODE_MINUS = 82
KEYCODE_PLUS = 86
KEYCODE_STAR = 63
KEYCODE_SLASH = 106
KEYCODE_PGUP = 117
KEYCODE_PGDOWN = 112
KEYCODE_CLOSING_BRACKET = 51
KEYCODE_OPEN_BRACKET = 48

MOVE_LEFT = 1000
MOVE_DOWN = 2000

# Mapping for mplayer

ACTIONS = {BTN_UP: KEYCODE_PGUP,
            BTN_DOWN: KEYCODE_PGDOWN,
            BTN_LEFT: KEYCODE_DOWN,
            BTN_RIGHT: KEYCODE_UP,
            BTN_A: KEYCODE_P,
            BTN_B: KEYCODE_F,
            BTN_1: KEYCODE_OPEN_BRACKET,
            BTN_2: KEYCODE_CLOSING_BRACKET,
            BTN_MINUS: KEYCODE_SLASH,
            BTN_PLUS: KEYCODE_STAR,
            BTN_HOME: KEYCODE_Q,
            MOVE_LEFT: KEYCODE_DOWN,
            MOVE_DOWN: KEYCODE_UP}

# Only Works with gnome
def press_key(keycode):
    """Simulate key being pressed and released."""
    pyatspi.Registry.generateKeyboardEvent(keycode, None,
                                           pyatspi.KEY_PRESSRELEASE)


class Remote(object):

    def main(self, wm):
        """Start Remote."""
        print "Ahora podés empezar a usar el control remoto !!!"
        print "Presioná el boton HOME del Wiimote para salir..."
        buttons = 0
        while buttons != BTN_HOME:
            acc = wm.acceleration
            buttons = wm.buttons
            pitch, roll, yawn = wm.positions

            action = buttons

            # Moving wiimote down.
            if acc[Z] > 200 and acc[X] < 200:
                action = MOVE_DOWN

            if action != 0:
                try:
                    press_key(ACTIONS[action])
                except:
                    print "Action no registered for button: %s" % action
                time.sleep(0.25)

if __name__ == '__main__':
    wm = WiiMote()
    wm.initialize()
    remote = Remote()
    remote.main(wm)
