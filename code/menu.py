
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTION, COLOR_WHITE, COLOR_GREEN


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu/Menubg.jpeg')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu/Musicmenu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(text_size=70, text= "THE", text_color= COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 70))
            self.menu_text(text_size=70, text="FALL", text_color= COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 150))
            self.menu_text(text_size=70, text="OF", text_color= COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 230))
            self.menu_text(text_size=70, text="CITY", text_color= COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 310))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(text_size=50, text= MENU_OPTION[i], text_color= COLOR_GREEN,
                               text_center_pos=((WIN_WIDTH / 2), 550 + 60 *i))
                else:
                    self.menu_text(text_size=50, text=MENU_OPTION[i], text_color=COLOR_WHITE,
                                   text_center_pos=((WIN_WIDTH / 2), 550 + 60 * i))
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Close Window
                    quit() # End pygame

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: # DOWN KY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP: # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_RETURN: # ENTER
                        return MENU_OPTION[menu_option]




    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
