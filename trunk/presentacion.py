# This code is so you can run the samples without installing the package
# -*- encoding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ejemplos/lib'))
import cwiid
from motes import Motes

import cocos
from cocos.director import director

import pyglet
from pyglet import font, image
from pyglet.gl import *
from pyglet.window import key

from cocos.actions import *
from cocos.layer import *
from cocos.scenes.transitions import *
#from cocos.sprite import *
from cocos import text

        
class BackgroundLayer(Layer):
    """
    """
    def __init__( self, path_name ):
        super(BackgroundLayer, self).__init__()
        self.image = image.load(path_name)
        
    def draw(self):
        texture = self.image.texture
        
        rx = director.window.width - 2*director._offset_x
        ry = director.window.height - 2*director._offset_y
        
        tx = float(rx)/texture.width
        ty = float(ry)/texture.height

        glEnable(GL_TEXTURE_2D)        
        glBindTexture(texture.target, texture.id)

        x, y = director.get_window_size()
        glBegin(gl.GL_QUADS)
        glTexCoord2d(0,0);
        glVertex2f( 0, 0 )
        glTexCoord2d(0,ty);
        glVertex2f( 0, y )
        glTexCoord2d(tx,ty);
        glVertex2f( x, y )
        glTexCoord2d(tx,0);
        glVertex2f( x,0 )
        glEnd()
        glDisable(GL_TEXTURE_2D)
        

class TitleSubTitleLayer(cocos.layer.Layer):
    def __init__(self, title, subtitle):
        super(TitleSubTitleLayer, self).__init__()

        x, y = director.get_window_size()

        self.title = text.Label(
                title, (x/2, y/2+50), font_name = 'Gill Sans',
                font_size = 64, anchor_x='center', anchor_y='center' )
        self.add( self.title )
        
        self.subtitle = text.Label(
                subtitle, (x/2, y/2-30), font_name = 'Gill Sans',
                font_size = 38, anchor_x='center', anchor_y='center' )
        self.add( self.subtitle )
        
class BulletListLayer(cocos.layer.Layer):
    def __init__(self, title, lines, orientation = "center"):
        super(BulletListLayer, self).__init__()
        x, y = director.get_window_size()

        self.title = text.Label(
                title, (x/2, y-50), font_name = 'Gill Sans',
                font_size = 50, anchor_x='center', anchor_y='center' )
        self.add( self.title )

        start_y = (y/12)*8
        font_size = 52 / (len(lines)/2.2+1)
        font_size = min(font_size, 52)
        line_font = font.load('Gill Sans', font_size)
        tot_height = 0
        max_width = 0
        rendered_lines = []
        step = 300/ max(len(lines),1)
        if orientation == "left":
            x = 300;
        i = 0
        for line in lines:
            line_text = text.Label(
                line, (x/2, y-150-step*i), font_name = 'Gill Sans',
                font_size = font_size, anchor_x='center', anchor_y='center' )
            i += 1   
            self.add( line_text )    

class TransitionControl(cocos.layer.Layer):
    is_event_handler = True
    
    def __init__(self, scenes, transitions=None):
        super(TransitionControl, self).__init__()
        
        self.transitions = transitions
        self.scenes = scenes
        for scene in scenes:
            if not self in scene.get_children():
                scene.add(self)
        self.scene_p = 0
        
    def next_scene(self):
        self.scene_p +=1 
        if self.scene_p >= len(self.scenes):
            self.scene_p = len(self.scenes)-1
        else:
            self.transition(self.transitions[self.scene_p%len(self.transitions)])
    
    def prev_scene(self):
        self.scene_p -=1 
        if self.scene_p < 0:
            self.scene_p = 0
        else:
            self.transition()
           
    def transition(self, transition=None):
        if transition:
            director.replace( transition(
                        self.scenes[ self.scene_p ],
                        duration = 1
                         )
                )
        else:
            director.replace( self.scenes[ self.scene_p ] )
        
    def on_key_press(self, keyp, mod):
        if keyp in (key.PAGEDOWN,key.RIGHT,key.UP,):
            self.next_scene()
        elif keyp in (key.PAGEUP,key.LEFT,key.DOWN,):
            self.prev_scene()
            

if __name__ == "__main__":

    director.init( resizable=True, width=800, height=600 ) 
    #director.window.set_fullscreen(True)
    background = BackgroundLayer("background.png")
    #background = cocos.layer.ColorLayer(0,0,0,255)
    #current_transition = 0

    scenes = [
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("/dev/wiimote",[" Experimentando con un wii-remote",
                " --= Autores =-- ",
                "Chr - chr@lanux.org.ar",
                "Ska - ska@lanux.org.ar",
                "Karucha - karucha@lanux.org.ar"
            ]),
        ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("/dev/wiimote",[" Temas",
                " Que es?, descripcion tecnica",
                " Como se usa en linux y en python",
                " Ejemplos con python, pygame y panda3d",
                " Proyecto Achuras ", 
                " Lanux y PyAr"
            ]),
        ),
        cocos.scene.Scene (background,
            BulletListLayer("Wii-Mote", [
                "Que es?",
                "Como se usa?",
                "--= Caracteristicas tecnicas =--",
                    "Acelerometro",
                    "Camara IR",
                    "Botones"
                ],"left")
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("Wii-Mote", [
                "Funciona en GNU/Linux?",
                "Libreria libcwiid",
                "+",
                "Bluetooth",
                ])
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("Wii-Mote", [
                "Ejemplos:",
                "wmgui",
                "# ejemplo1 - Wiiewer.py"
                ])
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("y Ahora que?", [
                "Pruebas realizadas en Lanux:",
                "--= Bateria =--",
                "# ejemplo2 bateria.py ",
                "# ejemplo3 bateria.py - (grafica)",
                "# ejemplo4 bateria.py- (palillos)"
                ])
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("Achuras Experience", [
                "http://www.achurasexperience.org",
                "Que es?",
                "Como se hizo?",
                "Mostramos juego",
                ])
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("Lanux - PyAr",  [
                "Reuniones",
                "Proyectos",
                "http://www.lanux.org.ar",
                "http://www.python.com.ar",
                ])
            ),
        cocos.scene.Scene (cocos.layer.ColorLayer(0,0,0,255),
            BulletListLayer("Gracias!!", [
                "",
                "Preguntas?",
                ])
            ),
        ]

    all_t = ['RotoZoomTransition','JumpZoomTransition',
            'SlideInLTransition','SlideInRTransition',
            'SlideInBTransition','SlideInTTransition',
            'FadeTransition']
            
            #Comentadas, por que fallan con algunas placas de video
            #'FlipX3DTransition',
            #'FlipY3DTransition', 'FlipAngular3DTransition'
            #'ShuffleTransition', 'TurnOffTilesTransition'
            #'FadeTRTransition', 'FadeBLTransition'
            #'FadeUpTransition', 'FadeDownTransition'
            #'ShrinkGrowTransition', 'CornerMoveTransition'
            #'EnvelopeTransition'
            #'SplitRowsTransition', 'SplitColsTransition'
    
    mytransitions = [ getattr(cocos.scenes.transitions, all_t[i % len(all_t)]) 
                for i in range(len(scenes)-1) ]
        
    #Inicializo los mandos del wiimote
    #wm = Motes()
    #wm.inicializarMandos()
    #if wm.wiimoteAvailable:
    #    acc, buttons = wm.returnStrenght()
    #    print buttons
    #    
    #    if buttons == cwiid.BTN_UP or buttons == cwiid.BTN_RIGHT:
    #        print "UP - RIGHT"
    #    if buttons == cwiid.BTN_DOWN or buttons == cwiid.BTN_LEFT:
    #        print "DOWN - LEFT"

    TransitionControl( scenes, mytransitions )
    director.run (scenes[0])

