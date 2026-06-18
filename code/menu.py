import pygame.image
from pygame.font import Font
from code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTION, COLOR_WHITE, COLOR_GREEN, WIN_HEIGHT
import webbrowser

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu/Menubg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

        # Fonts preloaded
        self.font_title = pygame.font.SysFont("Lucida Sans Typewriter", 70)
        self.font_option = pygame.font.SysFont("Lucida Sans Typewriter", 50)
        self.font_controls = pygame.font.SysFont("Arial", 20)

    def run(self, ):
        menu_option = 0
        pygame.mixer_music.load('./asset/Songs/Musicmenu.mp3')
        pygame.mixer_music.play(-1)
        while True:

            self.window.blit(self.surf, self.rect)

            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            # Draw Title and controls
            pos_y = 100
            for char in ["THE", "FALL","OF", "CITY"]:
                self.menu_text(self.font_title, char, COLOR_ORANGE, (WIN_WIDTH / 2, pos_y))
                pos_y += 80


            # Options
            for i in range(len(MENU_OPTION)):
                color = COLOR_GREEN if i == menu_option else COLOR_WHITE
                self.menu_text(self.font_option, MENU_OPTION[i], color, (WIN_WIDTH / 2, 550 + 60 * i))
            self.draw_controls()

            pygame.display.flip()


            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Close Window
                    quit() # End pygame

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_w:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_RETURN: # ENTER
                        return MENU_OPTION[menu_option]
    def draw_controls(self):

        start_y = 840
        overlay_height = 120

        overlay = pygame.Surface((300, overlay_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (WIN_WIDTH / 2 - 150, start_y))

        controls = [ "Controles",
                     "WASD - Movimentar",
                     "LSHIFT - Correr",
                     "MOUSE BOTÂO ESQUERDO - Atirar"
        ]

        y_offset = start_y + 20
        for line in controls:
            text_surf = self.font_controls.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(WIN_WIDTH / 2, y_offset))
            self.window.blit(text_surf, text_rect)
            y_offset += 25

    def draw_credits(self):
        self.window.fill((0, 0, 0))

        credits_data =  [
            ("CRÉDITOS", None), ("", None),
            ("Desenvolvido por: Humberto Gozzer", None), ("", None),
            ("--- ASSETS GRÁFICOS ---", None),
            ("CraftPix (Clique para abrir)", "https://craftpix.net"), ("", None),
            ("--- TRILHA SONORA E EFEITOS ---", None),
            ("Músicas (Cidade/Boss): Bogart VGM", None),
            ("Música (Menu): Patrick de Arteaga (Clique para abrir)", "patrickdearteaga.com"),
            ("Efeitos (Grito Boss): Dragon-Studio (Clique para abrir)", "https://ko-fi.com/dragonstudio"),
            ("", None), ("Pressione ENTER para voltar", None)

        ]
        self.link_rects = []
        y = 100
        for text,  link in credits_data:
            surf = self.font_controls.render(text, True, COLOR_WHITE)
            rect = surf.get_rect(center=(WIN_WIDTH // 2, y))
            self.window.blit(surf, rect)

            if link:
                self.link_rects.append((rect, link))
            y+= 40

        pygame.display.flip()

    def show_message(self, message):
        overlay = pygame.Surface((WIN_WIDTH, 200))
        overlay.set_alpha(200); overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 300))

        font = pygame.font.SysFont("Lucida Sans Typewriter", 80)
        text_surf = font.render(message, True,  (255, 0, 0))
        text_rect = text_surf.get_rect(center=(WIN_WIDTH / 2, 400))
        self.window.blit(text_surf, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)





    def menu_text(self, font:Font, text: str, text_color: tuple, text_center_pos: tuple):
        text_surf = font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
