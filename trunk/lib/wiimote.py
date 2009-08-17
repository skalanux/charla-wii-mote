#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cwiid, time
import struct
import math

class WiiMote(object):
    def initialize(self):
        try:
            print "Press button 1 and 2 of the wiimote..."
            wm = cwiid.Wiimote()
            #wm = cwiid.Wiimote('00:1E:35:DE:29:82')
            # Si se sabe la direccion del wiimote esto se podrìa llegar a
            # obviar
            print "Connection to the wiimote has been stablished"
            wm.rumble = 1
            time.sleep(.2)
            wm.rumble = 0
            accel_buf = wm.read(cwiid.RW_EEPROM, 0x15, 7)
            self._accel_calib = struct.unpack("BBBBBBB", accel_buf)
            self.wm = wm
            self.wm.rpt_mode = 31
        except Exception, e:
            print e
            print "Wiimote is not available, bytes...!!!!"
            raise

    def _get_acceleration(self):
        """Get acceleration on all axes."""
        acc = self.wm.state['acc']
        return acc
    acceleration  = property(_get_acceleration)

    def _get_ir_src(self):
        return self.wm.state['ir_src']
    ir_src = property(_get_ir_src)

    def _get_buttons(self):
        """Return buttons being pressed. """
        buttons = self.wm.state['buttons']
        return buttons
    buttons = property(_get_buttons)

    def _get_positions(self):
        """Return accelerometer spatial data."""
        #(xi, yi, zi), ir_src = self.wm.state['acc'], self.wm.state['ir_src']
        (xi, yi, zi) = self._get_acceleration()

        x = float(xi)
        y = float(yi)
        z = float(zi)

        # Weight the accelerations according to calibration data and
        # center around 0
        a_x = (x - self._accel_calib[0])/(self._accel_calib[4]-self._accel_calib[0])
        a_y = (y - self._accel_calib[1])/(self._accel_calib[5]-self._accel_calib[1])
        a_z = (z - self._accel_calib[2])/(self._accel_calib[6]-self._accel_calib[2])

        try:
            roll = math.atan(float(a_x)/float(a_z))
            if a_z<=0:
                    if (a_x>0):
                            roll -= math.pi
                    else:
                            roll += math.pi
            roll = -roll
            pitch = math.atan(a_y/a_z*math.cos(roll))
            accel = math.sqrt(math.pow(a_x,2)+math.pow(a_y,2)+math.pow(a_z,2))

            return pitch, roll, accel
            #return pitch, roll, accel, (a_x, a_y, a_z), ir_src
        except ZeroDivisionError:
            return 0,0,0
    positions  = property(_get_positions)

if __name__ == '__main__':
    wm = WiiMote()
    wm.initialize()
    print wm.positions
    print wm.acceleration
    print wm.buttons
    print wm.ir_src
