import cwiid, time
import threading 
import struct 
import math

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

    def returnStrenght(self):
        """
        Devuelve la fuerza aplicada en cada eje xyx
        Si es un mouse hay que medir la distancia recorrida en el tiempo, para simular una fuerza basada en la aceleracion
        para sacar las del mouse habria que usar panda esa es la cagada, o simplemente sacar las coordenadas del mouse por pantalla, para hacerlo
        generico es para ver o por ahi si esta disponible panda usarlo en una clase redefinida
        """
        #Si esta disponible panda y/o mouse se podria hacer esto:
        if self.wiimoteAvailable:
            acc, buttons = self.wm.state['acc'], self.wm.state['buttons']
            return acc, buttons
        else:
            #if base.mouseWatcherNode.hasMouse():
            #    accx = base.mouseWatcherNode.getMouseY()
            #    accy = base.mouseWatcherNode.getMouseY()
            #    accz = base.mouseWatcherNode.getMouseY() #Con este hay que tirotear algo       
            #    buttons = ??
            #    return accx, accy, accz, buttons    
            pass
            
    def checkMove(self, event):
        """
        Virtual Class
        """
        pass
    
    def getPitch(self):
        """
        Devuelve el pitch del wiimote
        """
        (xi, yi, zi), ir_src = self.wm.state['acc'], self.wm.state['ir_src']
        
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
        
            return pitch, roll, accel, (a_x, a_y, a_z), ir_src
        except ZeroDivisionError:
            return 0,0,0,(0,0,0), 0


if __name__ == "__main__":
    mote = Motes()
    mote.inicializarMandos()
    while 1==1:
        print mote.getPitch()
        time.sleep(1)
