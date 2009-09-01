# -*- coding: iso-8859-1 -*-

import pygame
from pygame.locals import *
from gun import SCREEN_WIDTH, SCREEN_HEIGHT, screen
class patoSprite(pygame.sprite.Sprite):
    def loadimage(self, action):
        if action == 1:
            self.image = pygame.image.load("images/PatoLucas.png")
        else:
            self.image = pygame.image.load("images/PatoLucas2.png")

        self.rect = self.image.get_rect()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadimage(1)

    def accert():
        self.loadimage(2)

class miraSprite(pygame.sprite.Sprite):
    SPEED = 10
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/mira.png")
        self.rect = self.image.get_rect()
        self.rect.center  = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def movs(self, dx, dy):
        self.rect.move_ip((dx * self.SPEED, dy * self.SPEED))
        self.rect.clamp_ip( screen.get_rect() )
