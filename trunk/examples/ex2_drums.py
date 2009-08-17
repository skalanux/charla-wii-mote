#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pyatspi
import sys
import time


from cwiid import BTN_A, BTN_MINUS, BTN_PLUS, BTN_LEFT, BTN_RIGHT, BTN_DOWN, \
    BTN_UP, BTN_B, BTN_1, BTN_2, BTN_HOME, X, Z, Y

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))
from wiimote import WiiMote

# Constants
POS_1 = 0
POS_2 = 1
POS_3 = 2
POS_4 = 3
POS_5 = 4

# Calibration

CALIBRATION_SLEEP_TIME = 0.5
THRESHOLD_SOUND_REPEAT = 0.05

THRESHOLD_MAX_X_LEVEL = 2
THRESHOLD_MAX_Z_LEVEL = 4
THRESHOLD_MIN_X_LEVEL = 1
THRESHOLD_MIN_Z_LEVEL = 2


BUTTONS_CALIBRATION = (BTN_MINUS, BTN_PLUS, BTN_UP, BTN_DOWN, BTN_LEFT,
                      BTN_RIGHT)

BUTTONS_MODIFIERS = (BTN_A, BTN_B, BTN_1, BTN_2)
# Sounds

SOUND_HAND_CLAP = 3
SOUND_SNARE_ROCK = 4
SOUND_RIDE_JAZZ = 12


SOUND_SNARE_JAZZ = 0
SOUND_TOM_HI = 1
SOUND_TOM_LOW = 2
SOUND_TOM_MID = 3
SOUND_KICK = 4


SOUND_CLOSED_HH = 0
SOUND_STICK = 1
SOUND_PEDAL_HH = 2
SOUND_OPEN_HH = 3
SOUND_COWBELL = 4

# Hacer que el boton de atras tenga los hihats, que para abajo sea bombo,
# ponerle threshold com constante

# Keycodes

KEYCODE_Z = 52
KEYCODE_S = 39
KEYCODE_X = 53
KEYCODE_D = 40
KEYCODE_C = 54
KEYCODE_V = 55
KEYCODE_G = 42
KEYCODE_B = 56
KEYCODE_H = 43
KEYCODE_N = 57
KEYCODE_J = 44
KEYCODE_K = 45
KEYCODE_M = 58

# Mapping

SOUND_KICK = KEYCODE_Z
SOUND_STICK = KEYCODE_S
SOUND_SNARE_JAZZ= KEYCODE_X
SOUND_HAND_CLAP= KEYCODE_D
SOUND_SNARE_ROCK= KEYCODE_C
SOUND_TOM_LOW= KEYCODE_V
SOUND_CLOSED_HH= KEYCODE_G
SOUND_TOM_MID= KEYCODE_B
SOUND_PEDAL_HH= KEYCODE_H
SOUND_TOM_HI= KEYCODE_N
SOUND_OPEN_HH= KEYCODE_J
SOUND_COWBELL= KEYCODE_M


SET_1 = (SOUND_OPEN_HH,
        SOUND_STICK,
        SOUND_PEDAL_HH,
        SOUND_CLOSED_HH,
        SOUND_COWBELL)

SET_2 = (SOUND_SNARE_JAZZ,
         SOUND_TOM_HI,
         SOUND_TOM_LOW,
         SOUND_TOM_MID,
         SOUND_KICK)

def press_key(keycode):
    """Simulate key being pressed and released."""
    pyatspi.Registry.generateKeyboardEvent(keycode, None,
                                           pyatspi.KEY_PRESSRELEASE)

class Ring(object):
    def __init__(self, size, initial_value=0, values=None):
        self.size = size
        self.index = initial_value
        if values == None:
            self.values = range(size)
        else:
            self.values = values

    def next(self):
        if self.index >= self.size - 1:
            self.index = 0
        else:
            self.index += 1

        return self.values[self.index]

    def prev(self):
        if self.index == 0:
            self.index = self.size - 1
        else:
            self.index -= 1

        return self.values[self.index]

    def _get_value(self):
        return self.values[self.index]
    value = property(_get_value)


class Drums(object):
    def __init__(self, wm):
        """Initialized Drums."""
        self.repeat = 0
        self.wm = wm

        # Sound threshold
        thresholds = map(lambda x:float(x)/1000, range(0,500,5))
        size_thresholds = len(thresholds)
        self.sound_threshold = Ring(size_thresholds, size_thresholds / 4, \
                                    thresholds)

        # Axes thresholds
        thresholds = range(180,230,10)
        size_thresholds = len(thresholds)


        self.threshold_min_x = Ring(size_thresholds, THRESHOLD_MIN_X_LEVEL, \
                                    thresholds)
        self.threshold_max_x = Ring(size_thresholds, THRESHOLD_MAX_X_LEVEL, \
                                    thresholds)

        self.threshold_min_z = Ring(size_thresholds, THRESHOLD_MIN_Z_LEVEL, \
                                    thresholds)
        self.threshold_max_z = Ring(size_thresholds, THRESHOLD_MAX_Z_LEVEL, \
                                    thresholds)

    def play(self, position):
        """Play an instrument."""
        sound_set = SET_2 if self.modifier else SET_1
        keycode = sound_set[position]
        press_key(keycode)
        if not self.repeat:
            time.sleep(self.sound_threshold.value)
        else:
            wm = self.wm
            buttons = wm.buttons
            # Find out how to check for multiple buttons pressed at the same
            # time
            while buttons == BTN_B:
                press_key(keycode)
                time.sleep(THRESHOLD_SOUND_REPEAT)
                buttons = wm.buttons

    def calibrate(self, buttons):
        """Calibrate thresholds."""
        if buttons == BTN_MINUS:
            self.sound_threshold.prev()
            print "Sound threshold: %s" % self.sound_threshold.value
            time.sleep(CALIBRATION_SLEEP_TIME)
        elif buttons == BTN_PLUS:
            self.sound_threshold.next()
            print "Sound threshold: %s" % self.sound_threshold.value
            time.sleep(CALIBRATION_SLEEP_TIME)

    def modify(self, buttons):
        """Modify behavior."""
        if buttons == BTN_1:
            self.modifier = 0
        if buttons == BTN_2:
            self.modifier = 1

        # Need to check for multiple buttons pressed at the same time
        if buttons == BTN_B:
            self.repeat = 1

    def start(self):
        """Start Drums."""
        print "Ahora podés empezar a usar la bateria !!!"
        print "Presioná el boton HOME del Wiimote para salir..."
        wm = self.wm
        buttons = 0
        self.modifier = 0
        while buttons != BTN_HOME:
            self.repeat = 0
            acc = wm.acceleration
            buttons = wm.buttons
            pitch, roll, yawn = wm.positions
            min_x = self.threshold_min_x.value
            max_x = self.threshold_max_x.value
            min_z = self.threshold_min_z.value
            max_z = self.threshold_max_z.value

            if buttons in BUTTONS_CALIBRATION:
                self.calibrate(buttons)

            if buttons in BUTTONS_MODIFIERS:
                self.modify(buttons)

            # Down
            if acc[Z] > min_z and acc[X] < max_x:
                self.play(POS_2)

            # Vertical movement
            #if acc[Y] > THRESHOLD_MIN_Y and acc[Z] < THRESHOLD_MAX_Z:
            #    self.play(POS_3, modifier)

            # Left
            if acc[X] > min_x and acc[Z] < max_z:
                self.play(POS_1)


if __name__ == '__main__':
    wm = WiiMote()
    wm.initialize()
    drum = Drums(wm)
    drum.start()
