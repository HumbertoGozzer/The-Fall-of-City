#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame import Rect

from code.const import WIN_WIDTH
from code.entity import Entity


class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.speed = 2

        self.animations = {
            'Run': pygame.image.load('./asset/Zombie/Zb1Run.png').convert_alpha(),
            'Attack': pygame.image.load('./asset/Zombie/Zb1Attack_1.png').convert_alpha(),
            'Dead': pygame.image.load('./asset/Zombie/Zb1Dead.png').convert_alpha()

        }
        self.current_state = 'Run'
        self.is_dead = False
        self.frame_index = 0.0
        self.frame_width = 96
        self.frame_height = 96
        self.scale_factor = 1.6
        self.last_attack_time = 0
        self.attack_cooldown = 500
        self.hitbox_width = int(self.frame_width * self.scale_factor *0.6)
        self.hitbox_height = int(self.frame_width * self.scale_factor *0.6)
        self.rect = pygame.Rect(position[0], position[1]
                                , self.hitbox_width, self.hitbox_height)

        self.render_offset_Y = 0
    def move(self, *args, **kwargs):
        if self.is_dead:
            self.current_state = 'Dead'
        elif not args:
            return
        else:
            player_rect = args[0]
            distancia_ataque = 60
            dx = player_rect.centerx - self.rect.centerx
            dy =  player_rect.centery - self.rect.centery

            if abs(dx) < distancia_ataque and abs(dy) < 30:
                if self.current_state != 'Attack': self.frame_index = 0.0
                self.current_state = 'Attack'
            else:
                if self.current_state != 'Run': self.frame_index = 0.0
                self.current_state  = 'Run'
                if dx > 0: self.rect.x += self.speed
                elif dx < 0: self.rect.x -= self.speed
                if dy > 0: self.rect.y += self.speed
                elif dy < 0: self.rect.y -= self.speed

            if self.current_state not in self.animations:
                self.current_state = 'Run'

        current_sheet = self.animations[self.current_state]
        total_frames = current_sheet.get_width() // self.frame_width

        if self.current_state == 'Dead':
            if self.frame_index < total_frames - 1:
                self.frame_index = 0.1
            else:
                self.frame_index = float(total_frames - 1)
        elif self.current_state == 'Attack':
            self.frame_index += 0.12

            if self.frame_index >= total_frames:
                self.frame_index = 0.0
        else:
            self.frame_index += 0.2
            if self.frame_index >= total_frames: self.frame_index = 0.0

        cut = pygame.Rect(int(self.frame_index) * self.frame_width, 0, self.frame_width, self.frame_height)
        frame = current_sheet.subsurface(cut)
        self.surf = pygame.transform.scale(frame, (int(self.frame_width * 1.6), 200))
        if not self.is_dead:
            dx = args[0].centerx - self.rect.centerx if args else 0
            if dx < 0:self.surf = pygame.transform.flip(self.surf, True, False)

