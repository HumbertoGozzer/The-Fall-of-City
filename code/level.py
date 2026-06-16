#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame

from code.const import COLOR_WHITE, WIN_HEIGHT, WIN_WIDTH
from code.enemy import Enemy
from code.entityFactory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):

        self.time_elapsed = 0
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 14)

        self.bg_list = EntityFactory.get_entity('onda1')
        self.entity_list = EntityFactory.get_entity('Player')
        self.bullet_list = []

    def run(self):

        pygame.mixer_music.load('./asset/Songs/Levelsong.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            tick = clock.tick(60)
            self.time_elapsed += tick

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Logic
            player = self.entity_list[0]

            if hasattr(player, 'new_bullet'):
                self.bullet_list.append(player.new_bullet)
                del player.new_bullet

            for ent in self.entity_list:
                if isinstance(ent, Enemy):
                    if not ent.is_dead: ent.move(player.rect)

                    if ent.rect.colliderect(player.rect) and ent.current_state == 'Attack':
                        if 2.0 <= ent.frame_index < 2.5:
                            if pygame.time.get_ticks() - ent.last_attack_time > ent.attack_cooldown:
                                player.take_damage()
                                ent.last_attack_time = pygame.time.get_ticks()

                else:
                    ent.move()

            for bullet in self.bullet_list:
                if bullet is None:
                    self.bullet_list.remove(bullet)
                    continue

                bullet.move()

                hit = False
                for ent in self.entity_list[:]:
                    if isinstance(ent, Enemy) and bullet.rect.colliderect(ent.rect):
                        ent.is_dead = True
                        hit = True
                        break

                if hit or bullet.rect.x < -100 or bullet.rect.x > WIN_WIDTH + 100:
                    if bullet in self.bullet_list:
                        self.bullet_list.remove(bullet)

            if self.time_elapsed > 5000:
                import random
                pos_x = random.choice([-100, WIN_WIDTH + 100])
                pos_y = random.randint(775, 950)
                new_enemy = EntityFactory.get_entity('Enemy', (pos_x, pos_y))
                self.entity_list.extend(new_enemy)
                self.time_elapsed -= 5000

            # Renderização
            self.window.fill((0, 0, 0))
            for bg in self.bg_list:
                self.window.blit(bg.surf, bg.rect)

            for bullet in self.bullet_list:
                self.window.blit(bullet.surf, bullet.rect)

            for ent in self.entity_list:
                draw_x = ent.rect.centerx - ent.surf.get_width() // 2
                offset_y = 15 if isinstance(ent, Enemy) else 0
                draw_y = ent.rect.bottom - ent.surf.get_height() + offset_y
                self.window.blit(ent.surf, (draw_x, draw_y))
                pygame.draw.rect(self.window, (255, 0, 0), ent.rect, 2)

            self.level_text(f'{self.name} - Tempo: {self.time_elapsed / 1000:.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()


    def level_text(self, text: str, text_color: tuple, text_pos: tuple):
        text_surf = self.font.render(text, True, text_color).convert_alpha()
        self.window.blit(text_surf, text_surf.get_rect(left=text_pos[0], top=text_pos[1]))
