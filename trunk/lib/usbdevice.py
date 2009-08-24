import pyatspi
import subprocess
import time

NUMLOCK_ON = ['/usr/bin/numlockx', 'on']
NUMLOCK_OFF = ['/usr/bin/numlockx', 'off']
NUMLOCK_TOGGLE = ['/usr/bin/numlockx', 'toggle']

XSET_SCROLL_ON = ['/usr/bin/xset', 'led', '3']
XSET_SCROLL_OFF = ['/usr/bin/xset', '-led', '3']

EVENT_BIT_1 = 0
EVENT_BIT_2 = 1
EVENT_BIT_ALL = 2

STATE_ON = 1
STATE_OFF = 0


EVENT_BIT_1 = {STATE_ON: XSET_SCROLL_ON,
               STATE_OFF: XSET_SCROLL_OFF
              }

EVENT_BIT_2 = {STATE_ON: NUMLOCK_ON,
               STATE_OFF: NUMLOCK_OFF
              }

EVENT_BIT_ALL_OFF = [EVENT_BIT_1[STATE_OFF],
                     EVENT_BIT_2[STATE_OFF]]

EVENT_BIT_ALL_ON = [EVENT_BIT_1[STATE_ON],
                     EVENT_BIT_2[STATE_ON]]

EVENT_BIT_ALL = {STATE_ON: EVENT_BIT_ALL_ON,
                STATE_OFF: EVENT_BIT_ALL_OFF
                }

class USBDevice(object):
    def _exec_commands(self, commands_list):
        for command in commands_list:
            subprocess.Popen(command)

    def _add_cmd(self, command_list, commands):
        if isinstance(commands[0], list):
            command_list.extend(commands)
        else:
            command_list.append(commands)

    def send_event(self, event=EVENT_BIT_ALL, state=STATE_ON):
        # First send off to all events
        command_off = EVENT_BIT_ALL_OFF
        commands_list = []
        self._add_cmd(commands_list, command_off)
        self._add_cmd(commands_list, event[state])
        self._exec_commands(commands_list)

if __name__ == "__main__":
    # TODO: High level function that set the different
    # states S0 S1 S2 S3
    usb_device = USBDevice()
    # Scroll ON:
    print "Scroll Lock on"
    usb_device.send_event(EVENT_BIT_1, STATE_ON)
    time.sleep(1)
    # NumLock ON
    print "Num Lock on"
    usb_device.send_event(EVENT_BIT_2, STATE_ON)
    time.sleep(1)
    # Both turned on
    print "Both ON"
    usb_device.send_event(EVENT_BIT_ALL, STATE_ON)
    time.sleep(1)
    # Both off
    print "Both OFF"
    usb_device.send_event(EVENT_BIT_ALL, STATE_OFF)
