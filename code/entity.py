#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame.image

class Entity(ABC):
    def __init__(self, name: str, position:tuple):
        self.name = name
        if not name.startswith('Background/') and name !='Enemy':
            self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
            self.rect = self.surf.get_rect(topleft=position)
        else:
            self.rect = pygame.Rect(position[0], position[1], 0, 0)

    @abstractmethod
    def move(self):
        pass
