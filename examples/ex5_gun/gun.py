#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

import cwiid
import pygame

from pygame.locals import *
from mysprites import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from wiimote import WiiMote

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
IMAGE_PATH = 'examples/ex5_gun/images/'
# Definimos la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Inicializamos pygame y sonido
pygame.mixer.pre_init(44100, -16, False)
pygame.init()

# Titulo
pygame.display.set_caption("Pistola!")

#Cargo la imagen del fondo y la muestro
fondo = pygame.image.load(IMAGE_PATH + '/fondo.png')
screen.blit(fondo, (0,0))


def main():

    # Cargo los Sprites
    mira = MiraSprite()
    pato = PatoSprite()

    mira_group = pygame.sprite.Group()
    mira_group.add(mira)
    mira_group.draw(screen)

    patos_group = pygame.sprite.Group()
    patos_group.add(pato)
    patos_group.draw(screen)

    # Inicializo los mandos del wiimote
    wm = WiiMote()
    try:
        wm.initialize()
    except:
        raise Exception

    playing = True
    while playing:
        # Chequeo el wiimote sino otorgo valores aleatorios para que no suene al
        # menos que se aprete la letra D

        try:
            ir_src = wm.ir_src[0]['pos']
            ir_pos_x = ir_src[0]
            ir_pos_y = ir_src[1]
        except:
            ir_pos_x = None
            ir_pos_y = None


        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    z = 2
                elif event.key == K_ESCAPE:
                    playing = False

        #Muevo el stick a donde dice el irSrcX
        if ir_pos_x is not None:
            ir_pos_x = SCREEN_WIDTH - ir_pos_x
            ir_pos_y = SCREEN_HEIGHT - ir_pos_y
            mira.rect.topleft = (ir_pos_x, ir_pos_y)

        # Verifico las colisiones
        collide_acerto = pygame.sprite.spritecollide(mira,patos_group,True)

        if collide_acerto:
            if ir_pos_x is None:
                #pato.load_image(2)
                #pygame.time.wait(100)
                patos_group.clear(screen, fondo)
                patos_group.draw(screen)
            else:
                #pygame.time.wait(100)
                patos_group.draw(screen)
                pato.load_image(1)

        mira_group.clear(screen, fondo)
        mira_group.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
