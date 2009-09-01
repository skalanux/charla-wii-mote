# -*- coding: iso-8859-1 -*-
from init import *
from random import randrange
import hollow
import glob, sys, time, cwiid
from motes import Motes
from sticksprite import *
#from quadrantReal import *
#from quadrantHelpers import *
import threading

mira = miraSprite()

def main():
    #Cargo todos los cuadrantes, el numero en un futuro podria llegar
    #a variar, de hecho seria piola sacarlos de un directorio
    #asi puedo crear mas y cargarlos on-demand
    #quadrants = [Quadrant1, Quadrant2, Quadrant3, Quadrant4, Quadrant5, Quadrant6, FondoVacio]

    #Cargo la imagen del fondo y la muestro
    fondo = pygame.image.load("images/fondo3.png")
    screen.blit(fondo, (0,0))

    # Titulo
    pygame.display.set_caption("Pistola!")

    # Cargo los Sprites
    StickSprite = pygame.sprite.Group()
    StickSprite.add(stick)

    #Creo el grupo de cuadrantes e iterando sobre la lista ya cargada los cargo
    #QuadrantSprite = pygame.sprite.Group()
    #for quad in quadrants:
    #    addQuadrant(QuadrantSprite,quad())

    #Luego muestro los cuadrantes por pantalla
    #QuadrantSprite.draw(screen)

    #Empezamos a tocar la bateria
    playing = True

    #Inicializo los mandos del wiimote
    wm = Motes()
    wm.inicializarMandos()

    while playing:
        #Chequeo el wiimote sino otorgo valores aleatorios para que no suene al
        #menos que se aprete la letra D
        try:
            pitch, roll, accel, (x,y,z), irSrc = wm.getPitch()
        except:
            pitch, roll, accel = 1 , 1, 1
            (x,y,z), irSrc =  (5,5,1), [{'pos': (720, 400), 'size': 1}]

        if wm.wiimoteAvailable:
            try:
                irSrcX = irSrc[0]['pos'][0]
                irSrcY = irSrc[0]['pos'][1]
            except:
                irSrcX = None
                irSrcY = None
        else:
            irSrcX = 720
            irSrcY = 400


        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    z = 2
                elif event.key == K_ESCAPE:
                    playing = False
                elif event.key == K_UP:
                    stick.movs(0,-1)
                elif event.key == K_DOWN:
                    stick.movs(0,1)
                elif event.key == K_LEFT:
                    stick.movs(-1,0)
                elif event.key == K_RIGHT:
                    stick.movs(1,0)


        #Muevo el stick a donde dice el ir
        if wm.wiimoteAvailable and irSrcX != None:
            irSrcX = 800 - irSrcX
            #irSrcX = (irSrcX * 0.4) + 200
            #irSrcY = (irSrcY * 0.4) + 180
            mira.rect.topleft = (irSrcX, irSrcY)

        # Verifico las colisiones
        collide_Acerto = pygame.sprite.spritecollide(mira,patosGroup,True)

        if collide_Acerto:
            if not collide_Quadrant[0].active:
                quad = collide_Quadrant[0]


                #Si colisiono y  el pitch esta en la posicion correcta,
                #hago sonar la bateria
                if z>1.5: #and pitch>-0.6 and pitch<0.03:
                    print irSrcX, irSrcY
                    #La intensidad del sonido depende de la aceleracion(fuerza)
                    def play():
                        quad.play(z*10)

                    threadplay = threading.Thread(target=play, name="thread1")
                    threadplay.start()
                    pygame.time.wait(100)
                #Cada vez que colisiona borro la pantalla y dibujo nuevamente
                QuadrantSprite.clear(screen, fondo)
                QuadrantSprite.draw(screen)
                #Marco el cuadrante como activo
                activateQuadrant(quadrants)
                addQuadrant(QuadrantSprite, quad)
            else:
                activateQuadrant(quadrants)
                QuadrantSprite.clear(screen, fondo)
                QuadrantSprite.draw(screen)
                quadrants = [Quadrant1, Quadrant2, Quadrant3, Quadrant4]

        StickSprite.clear(screen, fondo)
        StickSprite.draw(screen)
        pygame.display.flip()

    pygame.time.wait(100)
    pygame.quit()

if __name__ == "__main__":
    main()
