#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

from cwiid import BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT, BTN_A, BTN_B, BTN_1, BTN_2, \
    BTN_MINUS, BTN_PLUS, BTN_HOME, Z, X, Y

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from wiimote import WiiMote
from usbdevice import USBDevice, EVENT_BIT_1, EVENT_BIT_2, EVENT_BIT_ALL, \
    STATE_ON, STATE_OFF

THRESHOLD_PITCH_LEFT_MIN = -0.15
THRESHOLD_PITCH_LEFT_MAX = -1

THRESHOLD_PITCH_RIGHT_MIN = 0.15
THRESHOLD_PITCH_RIGHT_MAX = 1

class Autitux(object):

    def main(self, wm):
        """Start Remote."""
        print "Ahora podés empezar a usar el autitux !!!"
        print "Presioná el boton HOME del Wiimote para salir..."
        buttons = 0
        usb_device = USBDevice()
        while buttons != BTN_HOME:
            acc = wm.acceleration
            buttons = wm.buttons
            pitch, roll, acc = wm.positions

            action = buttons

            time.sleep(0.5)

            # Moving wiimote down.
            #if acc[Z] > 200 and acc[X] < 200:
            #    action = MOVE_DOWN


            """
            if pitch < THRESHOLD_PITCH_LEFT_MIN and \
                pitch > THRESHOLD_PITCH_LEFT_MAX:
                print "LEFT"
                usb_device.send_event(EVENT_BIT_1, STATE_ON)
                continue
            """


            if pitch < THRESHOLD_PITCH_LEFT_MIN and \
                pitch > THRESHOLD_PITCH_LEFT_MAX:
                print "LEFT"
                usb_device.send_event(EVENT_BIT_1, STATE_ON)
                continue

            if pitch > THRESHOLD_PITCH_RIGHT_MIN and \
                pitch < THRESHOLD_PITCH_RIGHT_MAX:
                print "RIGHT"
                usb_device.send_event(EVENT_BIT_2, STATE_ON)
                continue




            if action != 0:
                try:
                    press_key(ACTIONS[action])
                except:
                    print "Action no registered for button: %s" % action
                time.sleep(0.25)

if __name__ == '__main__':
    wm = WiiMote()
    wm.initialize()
    autitux = Autitux()
    autitux.main(wm)
