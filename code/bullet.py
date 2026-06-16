import pygame
from code.entity import Entity

class Bullet(Entity):
    def __init__(self,  position, turned_left):
        self.speed  = 10
        self.turned_left = turned_left

        self.surf = pygame.Surface((10, 5))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=position)

    def move(self):
        if self.turned_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed