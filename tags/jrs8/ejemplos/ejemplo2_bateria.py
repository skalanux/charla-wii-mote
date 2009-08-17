#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bateria"""
import os, sys
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, libdir)

import pygame, glob, time, cwiid
from motes import Motes

class baterias:
    def cargarsonidos(self,archivos):
        tags = []
        for nombre in archivos:
            tags.append(nombre)
        return tags
    
    def reproducir(self,archivo,porcvolumen):
        print "Reproduciendo : " + archivo
        pygame.mixer.music.load(archivo)
        volumen = porcvolumen / 100.0
        if volumen > 1.0 :
            volumen = 1.0
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play()

    def seleccionarsonido(self,nrotipodesonido,botonpresionado,seleccionado,sonidos):
        if seleccionado > 0 and (botonpresionado == cwiid.BTN_LEFT or botonpresionado == cwiid.BTN_UP):
            seleccionado = seleccionado - 1
            time.sleep(0.5)
        if seleccionado < len(sonidos)-1 and (buttons == cwiid.BTN_RIGHT or buttons == cwiid.BTN_DOWN):
            seleccionado = seleccionado + 1
            time.sleep(0.5)
        
        print "Sonido " + str(nrotipodesonido) + " seleccionado : (" + str(seleccionado) + ")  " + sonidos[seleccionado]
        return(seleccionado)

if __name__ == '__main__':
    #Inicializo el mixer de pygame
    try:
        pygame.mixer.init()
    except:
        print "Error en pygame.mixer.init() en setup_everything():"
        print sys.exc_info()[0],":",sys.exc_info()[1]

    #Leo todos los archivos
    archivosplatillos = glob.glob ('sound/platillos/*.ogg')
    archivosbombos = glob.glob ('sound/bombos/*.ogg')
    bateria = baterias()
    sonidosplatillos = bateria.cargarsonidos(archivosplatillos)
    sonidosbombos = bateria.cargarsonidos(archivosbombos)

    wm = Motes()
    #Inicializo los mandos del wiimote
    wm.inicializarMandos()
    if wm.wiimoteAvailable:
        print "Ahora puede empezar a usar la bateria !!!"
        print "Presione el boton A del Wiimote para salir..."
        sonidoseleccionado1=0
        sonidoseleccionado2=2
        buttons = 0
        ledsonido1 = 1
        ledsonido2 = 1
        wm.led=ledsonido1
        while buttons != cwiid.BTN_A :
            acc, buttons = wm.returnStrenght()
            valor1 = acc[cwiid.X]-200 
            valor2 = acc[cwiid.Z]-220 
            maximo1 = 20
            maximo2 = 30
            porcentaje1 = valor1 * 100 / maximo1
            porcentaje2 = valor2 * 100 / maximo2
            
            #Seleccionando Sonidos
            if buttons == cwiid.BTN_LEFT or buttons == cwiid.BTN_RIGHT:
                sonidoseleccionado1=bateria.seleccionarsonido(1,buttons,sonidoseleccionado1,sonidosplatillos)
                ledsonido1=ledsonido1+1
                wm.led = ledsonido1
            if buttons == cwiid.BTN_UP or buttons == cwiid.BTN_DOWN:
                #sonidoseleccionado2=bateria.seleccionarsonido(2,buttons,sonidoseleccionado2,sonidosplatillos)
                sonidoseleccionado2=bateria.seleccionarsonido(2,buttons,sonidoseleccionado2,sonidosbombos)
                ledsonido2=ledsonido2+1
                wm.led = ledsonido2
                
            moteData = wm.getPitch()
            pitch = moteData[0]

            if acc[cwiid.X] > 190 and acc[cwiid.Z] < 220: # and pitch > 0.6 and pitch < 0.8: 
                print pitch
                bateria.reproducir(sonidosplatillos[sonidoseleccionado1],porcentaje1)
                time.sleep(0.05)
            if acc[cwiid.Z] > 200 and acc[cwiid.X] < 200 and pitch > 0 and pitch < 0.3:
                print acc[2]
                #Magia, suena
                bateria.reproducir(sonidosbombos[sonidoseleccionado2],porcentaje2)
                time.sleep(0.05)

