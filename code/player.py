#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.key
from pygame import Rect

from code.bullet import Bullet
from code.const import WIN_WIDTH
from code.entity import Entity


class Player(Entity):
    def __init__(self, name: str, position):
        super().__init__(name, position)
        self.last_hit_time = 0
        self.new_bullet = None
        self.name= 'Player'

        self.hp = 100
        self.is_dead = False
        self.has_fired = False

        self.last_shot_time = 0
        self.shot_cooldown = 200

        # Loading of the animations
        self.animations = {
            'Idle': pygame.image.load('./asset/Soldier/Idle.png').convert_alpha(),
            'Walk': pygame.image.load('./asset/Soldier/Walk.png').convert_alpha(),
            'Run': pygame.image.load('./asset/Soldier/Run.png').convert_alpha(),
            'MeleAttack': pygame.image.load('./asset/Soldier/MeleAttack.png').convert_alpha(),
            'Shot': pygame.image.load('./asset/Soldier/Shot_2.png').convert_alpha(),
            'Dead': pygame.image.load('./asset/Soldier/Dead.png').convert_alpha()


        }
        # Animation settings and sizes
        self.current_action = 'Idle'
        self.index_frame = 0.0
        self.speed_animation = 0.10
        self.width_frame = 128
        self.height_frame = 128

        self.height_render = 200
        self.hitbox_width = 80
        self.hitbox_height = 120
        self.render_offset_Y = 80

        # Settings (flash red)
        self.is_flashing = False
        self.flash_duration = 0
        self.flash_frames = 10
        self.turned_left = False




        self.rect = Rect(position[0], position[1], self.hitbox_width, self.hitbox_height)
        self.animating()

    def get_bullet(self):
        bullet = self.new_bullet
        self.new_bullet = None
        return  bullet

    def move(self, can_move=True):

        if not can_move or self.current_action == 'Dead':
            self.current_action = 'Idle'
            self.animating()
            return

        pressed = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        in_moviment = any([pressed[pygame.K_w], pressed[pygame.K_s], pressed[pygame.K_a], pressed[pygame.K_d]])
        speed = 3 * (1.3 if pressed[pygame.K_LSHIFT] else 1.0)


        if mouse[0]:
            self.current_action = 'Shot'

            if mouse[0]:
                if 2.0 <= self.index_frame < 2.9:
                    current_time =  pygame.time.get_ticks()
                    if current_time - self.last_shot_time > self.shot_cooldown:
                        if self.new_bullet is None:
                            offset_x = -30 if self.turned_left else 30
                            bullet_pos = (self.rect.centerx + offset_x, self.rect.centery - 20)
                            self.new_bullet = Bullet(bullet_pos, self.turned_left)
                            self.last_shot_time = current_time
                            self.has_fired = True

            if self.index_frame > 3.0:
                self.has_fired = False


        elif in_moviment:
            self.current_action = 'Run' if pressed[pygame.K_LSHIFT] else 'Walk'
            if pressed[pygame.K_w]: self.rect.y -= speed
            if pressed[pygame.K_s]: self.rect.y += speed
            if pressed[pygame.K_a]:
                self.rect.x -= speed
                self.turned_left = True
            if pressed[pygame.K_d]:
                self.rect.x += speed
                self.turned_left = False

        else:
                self.current_action = 'Idle'

        # Screen limits
        self.rect.clamp_ip(pygame.Rect(0, 775, WIN_WIDTH, 300))
        self.animating()

    def animating(self):

        current_sheet = self.animations[self.current_action]
        total_frames = current_sheet.get_width() // self.width_frame

        if self.current_action == 'Dead' and int(self.index_frame) == total_frames - 1:
            self.index_frame = total_frames - 1
        else:

            self.index_frame += self.speed_animation
            if self.index_frame >= total_frames:
                self.index_frame = 0.0

        cut = Rect(int(self.index_frame) * self.width_frame, 0, self.width_frame, self.height_frame)
        original_frame = current_sheet.subsurface(cut)
        self.surf = pygame.transform.scale(original_frame, (int(self.width_frame * 1.5), self.height_render))

        if self.turned_left:
            self.surf = pygame.transform.flip(self.surf, True, False)

        if self.is_flashing:

            mask = pygame.mask.from_surface(self.surf)
            red_silhouette = mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor =(0, 0, 0, 0))
            red_silhouette.set_alpha(180)
            self.surf.blit(red_silhouette, (0, 0))
            self.flash_duration -= 1
            if self.flash_duration <= 0: self.is_flashing = False

    def take_damage(self, damage_amount):
        if not self.is_flashing and not self.is_dead:

            self.hp -= damage_amount
            if self.hp <= 0:
                self.is_dead = True
                self.current_action = 'Dead'
                self.index_frame = 0.0
            else:
                self.is_flashing = True
                self.flash_duration = self.flash_frames


