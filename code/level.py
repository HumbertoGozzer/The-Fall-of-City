#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame
import random

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
        self.music_playing = 'Levelsong'
        self.boss_scream_sound = pygame.mixer.Sound('./asset/Songs/Screamsong.wav')
        self.wave_count = 1
        self.enemies_killed = 0
        self.boss_spawned = False
        self.player_can_move = True
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

            self.player_can_move = True
            for ent in self.entity_list:
                if ent.name == 'Boss':
                    if ent.boss_event_step < 3:
                        self.player_can_move = False

                    if ent.boss_event_step == 0:
                        if ent.rect.centerx > WIN_WIDTH / 1.5:
                            ent.rect.x -= 4

                        else:
                            ent.boss_event_step = 1


                    if ent.boss_event_step == 1:
                        if ent.current_state != 'Scream':
                            ent.current_state = 'Scream'
                            ent.frame_index = 0.0
                            self.boss_scream_sound.play()
                            ent.boss_event_step = 2

                    elif ent.boss_event_step == 2:
                        total_frames_scream = ent.animations['Scream'].get_width() // ent.frame_width
                        if ent.frame_index >= (total_frames_scream - 0.5):
                            self.boss_scream_sound.stop()
                            pygame.mixer_music.load('./asset/Songs/bossfight.mp3')
                            pygame.mixer_music.play(-1)
                            ent.boss_event_step = 3
                            ent.current_state = 'Run'

            player = self.entity_list[0]
            player.move(can_move=self.player_can_move)
            new_bullet = player.get_bullet()
            if new_bullet is not None:
                self.bullet_list.append(new_bullet)

            for ent in self.entity_list[:]:
                if isinstance(ent, Enemy):
                    if ent.is_dead:
                        total_frames = ent.animations['Dead'].get_width() // ent.frame_width

                        if ent.current_state == 'Dead' and ent.frame_index >= (total_frames - 0.2):
                            self.entity_list.remove(ent)
                            self.enemies_killed += 1
                        else:
                            ent.move()
                        continue

                    ent.move(player.rect)

                    if ent.rect.colliderect(player.rect) and 'Attack' in ent.current_state:
                        if int(ent.frame_index) == getattr(ent, 'attack_frame', 2):
                            if pygame.time.get_ticks() - ent.last_attack_time > ent.attack_cooldown:
                                damage = getattr(ent, 'attack_damage', 10)
                                player.take_damage(damage)
                                ent.last_attack_time = pygame.time.get_ticks()

                else:
                    ent.move()
            # Generator of waves
            if self.wave_count == 1 and self.enemies_killed >= 5:
                self.wave_count = 2
                self.enemies_killed = 0
            elif self.wave_count == 2 and self.enemies_killed >= 15 and not self.boss_spawned:
                self.start_boss_event()


            if self.time_elapsed > (3000 / self.wave_count):
                if self.wave_count < 3:
                    pos_x = random.choice([-100, WIN_WIDTH + 100])
                    pos_y = random.randint(775, 950)
                    tipo = 'Zb1' if self.wave_count == 1 else ('Zb2' if self.wave_count == 2 else random.choice(['Zb1', 'Zb2']))
                    new_enemy = EntityFactory.get_entity('Enemy', (pos_x, pos_y, tipo))
                    new_enemy[0].speed = 2 + self.wave_count
                    self.entity_list.extend(new_enemy)
                self.time_elapsed = 0


            for bullet in self.bullet_list[:]:
                bullet.move()

                hit = False


                for ent in self.entity_list[:]:
                    if isinstance(ent, Enemy) and not ent.is_dead and bullet.rect.colliderect(ent.rect):
                        if ent.name == 'Boss':
                            ent.hp -= 10
                            if ent.hp <= 0: ent.is_dead = True
                        else:
                            ent.is_dead = True

                        hit = True
                        break
                if hit or bullet.rect.x < -100 or bullet.rect.x > WIN_WIDTH + 100:
                    if bullet in self.bullet_list:
                        self.bullet_list.remove(bullet)

            if player.is_dead:
                return False

            boss = next((ent for ent in self.entity_list if ent.name == 'Boss'), None)
            if boss is not None:
                if  boss.hp <= 0:
                    return True

            # Renderização
            self.window.fill((0, 0, 0))
            for bg in self.bg_list: self.window.blit(bg.surf, bg.rect)
            for bullet in self.bullet_list: self.window.blit(bullet.surf, bullet.rect)

            for ent in self.entity_list:

                draw_x = ent.rect.centerx - ent.surf.get_width() // 2
                offset_y = 15 if isinstance(ent, Enemy) else 0
                draw_y = ent.rect.bottom - ent.surf.get_height() + offset_y
                self.window.blit(ent.surf, (draw_x, draw_y))
                pygame.draw.rect(self.window, (255, 0, 0), ent.rect, 2)

                if ent.name == 'Boss' and not ent.is_dead:
                    pygame.draw.rect(self.window, (50, 50, 50), (WIN_WIDTH // 4, 30, WIN_WIDTH // 2, 20))
                    vida_percentual = max(0, ent.hp / 500)
                    pygame.draw.rect(self.window, (200, 0, 0),
                                     (WIN_WIDTH // 4, 30, (WIN_WIDTH // 2) * vida_percentual, 20))

            self.level_text(f'{self.name} - Onda: {self.wave_count} |Mortes: {self.enemies_killed}', COLOR_WHITE, (10, 5))
            self.level_text(f'{self.name} - Tempo: {self.time_elapsed / 1000:.1f}s', COLOR_WHITE, (10, 25))
            self.level_text(f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()

    def start_boss_event(self):
        self.boss_spawned = True
        self.wave_count = 3
        pygame.mixer.music.stop()

        # Spawn boss
        boss = EntityFactory.get_entity('Enemy', (WIN_WIDTH + 100, 850, 'Boss'))
        boss[0].current_state = 'Walk'
        boss[0].boss_event_step = 0
        boss[0].hp = 500
        boss[0].attack_damage = 20
        self.entity_list.extend(boss)


    def level_text(self, text: str, text_color: tuple, text_pos: tuple):
        text_surf = self.font.render(text, True, text_color).convert_alpha()
        self.window.blit(text_surf, text_surf.get_rect(left=text_pos[0], top=text_pos[1]))
