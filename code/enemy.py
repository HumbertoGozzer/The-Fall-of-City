#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import pygame

from code.entity import Entity

class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__('Enemy', position)
        self.name = name
        self.speed = 2

        self.hp = 1
        if self.name == 'Boss':
            self.hp = 500
            self.animations = {
                'Idle': pygame.image.load(f'./asset/Zombie/bossIdle.png').convert_alpha(),
                'Walk': pygame.image.load(f'./asset/Zombie/bossWalk.png').convert_alpha(),
                'Run': pygame.image.load(f'./asset/Zombie/bossRun.png').convert_alpha(),
                'Jump': pygame.image.load(f'./asset/Zombie/bossJump.png').convert_alpha(),
                'Scream': pygame.image.load(f'./asset/Zombie/bossScream.png').convert_alpha(),
                'Dead': pygame.image.load(f'./asset/Zombie/bossDead.png').convert_alpha(),
                'Attack1': pygame.image.load(f'./asset/Zombie/bossAttack_1.png').convert_alpha(),
                'Attack2': pygame.image.load(f'./asset/Zombie/bossAttack_2.png').convert_alpha(),
                'Attack3': pygame.image.load(f'./asset/Zombie/bossAttack_3.png').convert_alpha()
            }
        else:
            self.animations = {
                'Run': pygame.image.load(f'./asset/Zombie/{self.name}Run.png'),
                'Attack': pygame.image.load(f'./asset/Zombie/{self.name}Attack_1.png'),
                'Dead': pygame.image.load(f'./asset/Zombie/{self.name}Dead.png')
            }
        self.current_state = 'Run'
        self.boss_event_step = 0
        self.is_dead = False
        self.death_flip  = False
        self.frame_index = 0.0
        self.frame_width = 96
        self.frame_height = 96
        self.scale_factor = 1.6
        self.last_attack_time = 0
        self.attack_cooldown = 500
        self.attack_frame = 2
        self.anim_speed = 0.10

        self.surf = pygame.transform.scale(self.animations['Run'].subsurface((0,0,self.frame_width,self.frame_height)), (int(self.frame_width * 1.6), 200))
        self.hitbox_width = int(self.frame_width * self.scale_factor *0.6)
        self.hitbox_height = int(self.frame_width * self.scale_factor *0.6)
        self.rect = pygame.Rect(position[0], position[1]
                                , self.hitbox_width, self.hitbox_height)

        self.render_offset_Y = 0
    def move(self, *args, **kwargs):
        if self.is_dead:
            self.current_state = 'Dead'
        elif args:
            player_rect = args[0]
            distancia_ataque = 60
            dx = player_rect.centerx - self.rect.centerx
            dy =  player_rect.centery - self.rect.centery

            if abs(dx) < distancia_ataque and abs(dy) < 30:
                if self.name == 'Boss' and self.boss_event_step == 3:
                    if self.current_state not in ['Attack1', 'Attack2', 'Attack3']:
                        self.frame_index = 0.0
                        self.current_state = random.choice(['Attack1', 'Attack2', 'Attack3'])
                else:
                    if self.current_state != 'Attack':
                        self.frame_index = 0.0
                        self.current_state = 'Attack'

            else:
                if self.name == 'Boss' and self.boss_event_step <3:
                    pass
                else:
                    if self.current_state != 'Run': self.frame_index = 0.0
                    self.current_state  = 'Run'
                    if dx > 0: self.rect.x += self.speed
                    elif dx < 0: self.rect.x -= self.speed
                    if dy > 0: self.rect.y += self.speed
                    elif dy < 0: self.rect.y -= self.speed

        if self.current_state not in self.animations:
            self.current_state = 'Idle' if self.name == 'Boss' else 'Run'

        current_sheet = self.animations[self.current_state]
        total_frames = current_sheet.get_width() // self.frame_width
        if self.current_state == 'Scream':
            self.frame_index += 0.03
        elif self.current_state == 'Dead':
            self.frame_index += 0.05
            if self.frame_index >= total_frames:
                self.frame_index = float(total_frames - 1)
        elif 'Attack' in self.current_state:
            self.frame_index += self.anim_speed
            if self.frame_index >= total_frames:
                self.frame_index = 0.0
                if self.name == 'Boss':
                    self.current_state = 'Run'
        else:
            self.frame_index += self.anim_speed
            if self.frame_index >= total_frames: self.frame_index = 0.0

        cut = pygame.Rect(int(self.frame_index) * self.frame_width, 0, self.frame_width, self.frame_height)
        frame = current_sheet.subsurface(cut)
        self.surf = pygame.transform.scale(frame, (int(self.frame_width * 1.6), 200))

        if self.is_dead:
            if self.death_flip: self.surf = pygame.transform.flip(self.surf,True, False)
        else:
            if args:
                dx = args[0].centerx - self.rect.centerx if args else 0
                if dx < 0:
                    self.surf = pygame.transform.flip(self.surf, True, False)
                    self.death_flip = True
                else:
                    self.death_flip = False

