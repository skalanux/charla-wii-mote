#!/usr/bin/python

import time

import Xlib.display
import Xlib.X


class KBDLedInterface(object):
    def __init__(self):
            self.display = Xlib.display.Display()


    def get_kbd_state(self):
        return self.display.get_keyboard_control()

    def set_kbd_led_on(self):
        self.display.change_keyboard_control(led_mode=Xlib.X.LedModeOn)
        self.get_kbd_state()

    def set_kbd_led_off(self):
        self.display.change_keyboard_control(led_mode=Xlib.X.LedModeOff)
        self.get_kbd_state()


if __name__ == '__main__':
    led_interface = KBDLedInterface()
    for i in range(5):
        led_interface._set_kbd_led_on()
        time.sleep(1)
        led_interface._set_kbd_led_off()

        time.sleep(1)
