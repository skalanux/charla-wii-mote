# -*- coding: iso-8859-1 -*-
import pygame
from pygame.locals import *
import sys, time, cwiid
from motes import Motes
from mysprites import *

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# Definimos la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Inicializamos pygame y sonido
pygame.mixer.pre_init(44100, -16, False)
pygame.init()

# Titulo
pygame.display.set_caption("Pistola!")

#Cargo la imagen del fondo y la muestro
fondo = pygame.image.load("images/fondo.png")
screen.blit(fondo, (0,0))


def main():

    # Cargo los Sprites
    mira = miraSprite()
    pato = patoSprite()

    miraGroup = pygame.sprite.Group()
    miraGroup.add(mira)
    miraGroup.draw(screen)

    patosGroup = pygame.sprite.Group()
    patosGroup.add(pato)
    patosGroup.draw(screen)

    #Inicializo los mandos del wiimote
    wm = Motes()
    wm.inicializarMandos()

    playing = True
    while playing:
        #Chequeo el wiimote sino otorgo valores aleatorios para que no suene al
        #menos que se aprete la letra D
        pitch, roll, accel, (x,y,z), irSrc = wm.getPitch()
        if wm.wiimoteAvailable and irSrc[0]['pos'][0] != None:
            print irSrc
            irSrcX = irSrc[0]['pos'][0]
            irSrcY = irSrc[0]['pos'][1]

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    z = 2
                elif event.key == K_ESCAPE:
                    playing = False

        #Muevo el stick a donde dice el irSrcX
        print irSrcX, irSrcY
        if wm.wiimoteAvailable and irSrcX != None:
            irSrcX = 800 - irSrcX
            #irSrcX = (irSrcX * 0.4) + 200
            #irSrcY = (irSrcY * 0.4) + 180
            mira.rect.topleft = (irSrcX, irSrcY)

        # Verifico las colisiones
        collide_Acerto = pygame.sprite.spritecollide(mira,patosGroup,True)

        if collide_Acerto:
                pato.loadimage(2)
                pygame.time.wait(100)
                patosGroup.clear(screen, fondo)
                patosGroup.draw(screen)

        miraGroup.clear(screen, fondo)
        miraGroup.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()