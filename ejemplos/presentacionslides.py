import cwiid, time
import struct 
import math
import os

BUTTON_2 = 1
BUTTON_1 = 2
BUTTON_B = 4
BUTTON_A = 8
BUTTON_MINUS = 16
BUTTON_HOME = 128
BUTTON_LEFT = 256
BUTTON_RIGHT = 512
BUTTON_DOWN = 1024
BUTTON_UP = 2048
BUTTON_PLUS = 4096

CODE_A = 65 #spacio
CODE_B = 41 #f
CODE_PLUS = 63 #*
CODE_MINUS = 112 #/
CODE_HOME = 9 #escape
CODE_1 = 32 #o
CODE_2 = 55 #v
CODE_UP = 98 #flecha arriba
CODE_DOWN = 104 #flecha abajo
CODE_LEFT = 100 #flecha izquierda
CODE_RIGHT = 102 #flecha derecha
 
class Motes():
    def __init__(self):
        print "Inicializo la bandera wiimote"

    def inicializarMandos(self):
        """
        Clase usada para registrar los eventos tenidos en cuenta por el sistema
        """
        #trying to start wiimote
        
        try:
            print "Presiona los botones 1 y 2 en el wiimote..."
            wm = cwiid.Wiimote()
            print "Conexion exitosa!"
            wm.rumble = 1
            time.sleep(.2)
            wm.rumble = 0
            #self._accel_calib = wm.get_acc_cal(cwiid.EXT_NONE)[0] #Ver de usar esta despues por ahora me funca con los dos de abajo
            accel_buf = wm.read(cwiid.RW_EEPROM, 0x15, 7)
            self._accel_calib = struct.unpack("BBBBBBB", accel_buf)
            self.wm = wm
            self.wiimoteAvailable = 1
            #Ver si uso una funcion callback para evitar tener que llamar a getCoords siempre, de esa manera solo se refrecaria cuando hay un evento
            self.wm.rpt_mode = 31
        except:        
            print "Wiimote no disponible, conformate con el mouse ches!"
            self.wiimoteAvailable = 0

    def getInfo(self):
        """
        Return the data retrieved from the wiimote properly formatted and ordered
        """
        state = self.wm.state
        (xi, yi, zi), ir_src, buttons = state['acc'], state['ir_src'], state['buttons']
        
        x = float(xi)
        y = float(yi)
        z = float(zi)
        
        #Weight the accelerations according to calibration data and
        #center around 0
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
        
            return pitch, roll, accel, (a_x, a_y, a_z), ir_src, buttons 
        except ZeroDivisionError:
            return 0,0,0,(0,0,0), 0, 0

def actions(wminfo):
    pressed_button = wminfo[5]
    x,y,z = wminfo[3]
    pitch = wminfo[0] 
 
    def simulate_key_being_pressed_and_released(keycode, sleepFreq=0.8): 
        os.popen2("xsendkeycode "+str(keycode)+" 1")
        os.popen2("xsendkeycode "+str(keycode)+" 0")
        time.sleep(sleepFreq)

    if pressed_button == BUTTON_LEFT:
        simulate_key_being_pressed_and_released(CODE_LEFT)
    elif pressed_button == BUTTON_RIGHT:
        simulate_key_being_pressed_and_released(CODE_RIGHT)
    elif pressed_button == BUTTON_UP:
        simulate_key_being_pressed_and_released(CODE_UP)
    elif pressed_button == BUTTON_DOWN:
        simulate_key_being_pressed_and_released(CODE_DOWN)
    elif pressed_button == BUTTON_PLUS:
        simulate_key_being_pressed_and_released(CODE_PLUS)
    elif pressed_button == BUTTON_MINUS:
        simulate_key_being_pressed_and_released(CODE_MINUS)
    elif pressed_button == BUTTON_B:
        simulate_key_being_pressed_and_released(CODE_B)
    elif pressed_button == BUTTON_A:
        simulate_key_being_pressed_and_released(CODE_A)
    elif pressed_button == BUTTON_HOME:
        simulate_key_being_pressed_and_released(CODE_HOME)
    elif pressed_button == BUTTON_1:
        simulate_key_being_pressed_and_released(CODE_1)
    elif pressed_button == BUTTON_2:
        simulate_key_being_pressed_and_released(CODE_2)

    print pitch
    if z > 2.5 and pitch < 1 and pitch > 0.7:
        simulate_key_being_pressed_and_released(CODE_RIGHT, 1)
    elif z > 2.5 and pitch < 0.5:
        simulate_key_being_pressed_and_released(CODE_LEFT, 1)

if __name__ == "__main__":
    mote = Motes()
    mote.inicializarMandos()
    while 1==1:
        actions(mote.getInfo())
