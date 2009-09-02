# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *

from gun import SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_PATH

class PatoSprite(pygame.sprite.Sprite):
    def load_image(self, action):
        if action == 1:
            self.image = pygame.image.load(IMAGE_PATH + '/PatoLucas.png')
        else:
            self.image = pygame.image.load(IMAGE_PATH + '/PatoLucas2.png')

        self.rect = self.image.get_rect()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image(1)

    def acert():
        self.load_image(2)

class MiraSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGE_PATH + '/mira.png')
        self.rect = self.image.get_rect()
        self.rect.center  = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

