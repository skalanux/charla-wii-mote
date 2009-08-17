#!/usr/bin/python

# Copyright (c) 2006 Sam Hocevar <sam@zoy.org>
#
#    This program is free software. It comes without any warranty, to 
#    the extent permitted by applicable law. You can redistribute it
#    and/or modify it under the terms of the Do What The Fuck You Want
#    To Public License, Version 2, as published by Sam Hocevar. See
#    http://sam.zoy.org/wtfpl/COPYING for more details.

import pygame
from pygame.locals import QUIT
from bluetooth import BluetoothSocket, BluetoothError, L2CAP
import thread, time

WIDTH = 800  #512
HEIGHT = 256 # 256 Don't change this one
#ADDRESS = '00:1F:32:8C:A7:B0' # Cambiar por la mac del wiimote que estan probando, la mac se averigua con el comando "hcitool scan"
ADDRESS = '00:1E:35:DE:29:82' # Cambiar por la mac del wiimote que estan probando, la mac se averigua con el comando "hcitool scan"

# Listening thread
def listener():
    global connected, sensor
    fdin.settimeout(0.1)
    while connected == 1:
        try:
            msg = fdin.recv(23)
        except BluetoothError:
            continue
        if len(msg) >= 7:
            for c in range(3):
                sensor[c] = ord(msg[4 + c])
    fdin.close()
    fdout.close()
    connected = -1

# Try to connect to Wiimote
print 'connecting to Wiimote ' + ADDRESS + ', please press buttons 1 and 2'
fdin = BluetoothSocket(L2CAP)
fdin.connect((ADDRESS, 0x13))
fdout = BluetoothSocket(L2CAP)
fdout.connect((ADDRESS, 0x11))
if not fdin or not fdout:
    raise 'could not connect to Wiimote, check the address'
# Open window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0)
pygame.display.set_caption('Wiiewer')
# Run listener
old = [127] * 3
sensor = [127] * 3
connected = 1
thread.start_new_thread(listener, ())
fdout.send("\x52\x12\x00\x31")
# Main display loop
while connected == 1:
    pixels = pygame.surfarray.pixels3d(window)
    for c in range(3):
        for t in range(min(old[c], sensor[c]) + 1, max(old[c], sensor[c])):
            pixels[WIDTH - 3][t][c] = 255
        pixels[WIDTH - 2][sensor[c]][c] = 255
        old[c] = sensor[c]
    del pixels
    window.unlock()
    window.blit(window, (-1, 0))
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == QUIT:
            connected = 0
    time.sleep(0.01)
while connected == 0:
    time.sleep(0.01)
pygame.display.quit()
