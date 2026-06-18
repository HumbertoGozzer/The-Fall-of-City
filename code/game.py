#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import webbrowser

import pygame

from code.const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTION
from code.level import Level
from code.menu import Menu


class Game:
        def __init__(self):
            pygame.init()
            self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))


        def run(self):

            while True:
                menu = Menu(self.window)
                menu_return = menu.run()

                if menu_return == MENU_OPTION[0]: # New game
                    level = Level(self.window, 'Level1', menu_return)
                    level_result = level.run()

                    if level_result is False:
                        menu.show_message("GAME OVER")
                    elif level_result is True:
                        menu.show_message("VOCÊ VENCEU!")


                if menu_return == MENU_OPTION[1]: # Credits
                    self.run_credits(menu)

                elif menu_return == MENU_OPTION[2]: # Exit
                    pygame.quit()
                    quit()

                else:
                    pass
        @staticmethod
        def run_credits(menu_obj):
            waiting = True
            clock = pygame.time.Clock()
            while waiting:
                clock.tick(60)
                menu_obj.draw_credits()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = event.pos
                            for rect, link in menu_obj.link_rects:
                                if rect.collidepoint(mouse_pos):
                                    webbrowser.open(link)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting = False




