import sys

import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from main import main_game

BACKGROUND_COLOR = "#0A0A0A"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
GRAY = (150, 150, 150)
pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


def render(serf, font, number, list_menu):
    for i in list_menu:
        if number == i[5]:
            serf.blit(font.render(i[2], False, i[4]), (i[0], i[1]))
        else:
            serf.blit(font.render(i[2], False, i[3]), (i[0], i[1]))


class Menu:
    def __init__(self):
        self.list_point_main_menu = [(500, 200, 'Играть', RED, GRAY, 0),
                                     (500, 300, 'Настройки', RED, GRAY, 1),
                                     (500, 400, 'Правила', RED, GRAY, 2),
                                     (500, 500, 'Выход', RED, GRAY, 3)]
        self.list_point_menu_volume = [(100, 600, 'Обратно в меню', RED, GRAY, 0),
                                       (100, 400, 'Мелодия 1', RED, GRAY, 1),
                                       (300, 400, 'Мелодия 2', RED, GRAY, 2),
                                       (500, 400, 'Мелодия 3', RED, GRAY, 3)]
        self.list_point_menu_hero = [(250, 600, 'Рифжих', RED, GRAY, 0),
                                     (850, 600, 'Лэйхо', RED, GRAY, 2),
                                     (500, 650, 'Назад', RED, GRAY, 1)]
        self.list_point_menu_level = [(150, 300, 'Уровень 1', RED, GRAY, 0),
                                      (850, 300, 'Уровень 2', RED, GRAY, 1),
                                      (150, 600, 'Уровень 3', RED, GRAY, 2),
                                      (850, 600, 'Уровень 4', RED, GRAY, 3),
                                      (500, 650, 'Назад', RED, GRAY, 4)]

        self.font_menu = pygame.font.Font(None, 50)

        self.game_volume = 0.5
        self.menu_vol = 0.5
        self.music = 'data/game_music_1.mp3'

    def menu_volume(self):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
        slider_menu = Slider(screen, 500, 100, 500, 40, min=0, max=100, step=1,
                             initial=self.menu_vol * 100)
        box_menu = TextBox(screen, 1050, 100, 50, 50, fontSize=30)
        slider_game = Slider(screen, 500, 200, 500, 40, min=0, max=100, step=1, initial=self.game_volume * 100)
        box_game = TextBox(screen, 1050, 200, 50, 50, fontSize=30)
        box_menu.disable()
        box_game.disable()
        run_volume = True
        render(screen, self.font_menu, 0, self.list_point_menu_volume)
        point = int(self.music.split('.')[0][-1])
        play_game = False
        while run_volume:
            events = pygame.event.get()
            text_v_menu = self.font_menu.render("Громкость в меню", False, (255, 0, 0))
            screen.blit(text_v_menu, (100, 100))
            text_v_game = self.font_menu.render("Громкость в игре", False, (255, 0, 0))
            screen.blit(text_v_game, (100, 200))
            text_choose = self.font_menu.render("Выберите мелодию для проигрывания в игре", False, (255, 0, 0))
            screen.blit(text_choose, (100, 300))
            x, y = pygame.mouse.get_pos()
            self.menu_vol = slider_menu.getValue() / 100
            self.game_volume = slider_game.getValue() / 100
            box_menu.setText(slider_menu.getValue())
            box_game.setText(slider_game.getValue())
            pygame_widgets.update(events)
            for i in self.list_point_menu_volume:
                if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                    point = i[5]
                    break
                else:
                    point = -1
            render(screen, self.font_menu, point, self.list_point_menu_volume)
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    elif event.key == pygame.K_RIGHT:
                        if point < len(self.list_point_menu_volume) - 1:
                            point += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point >= 0:
                        if point == 0:
                            pygame.mixer.music.load('data/menu_music.mp3')
                            pygame.mixer.music.set_volume(self.menu_vol)
                            pygame.mixer.music.play(-1)
                            play_game = False
                            run_volume = False
                            screen.fill(BACKGROUND_COLOR)
                        else:
                            self.music = f'data/game_music_{point}.mp3'
                            pygame.mixer.music.load(self.music)
                            pygame.mixer.music.set_volume(self.game_volume)
                            pygame.mixer.music.play(-1, 1)
                            play_game = True
            if play_game:
                pygame.mixer.music.set_volume(self.game_volume)
            else:
                pygame.mixer.music.set_volume(self.menu_vol)

            pygame.display.update()
            pygame.display.flip()

        slider_menu.hide()
        slider_game.hide()
        box_menu.hide()
        box_game.hide()

    def menu_hero(self):
        screen.fill(BACKGROUND_COLOR)
        run_hero = True
        point = -1
        while run_hero:
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            rif = pygame.image.load('data/Рифжих.png')
            image1 = pygame.transform.scale(rif, (200, 200))
            screen.blit(image1, (220, 350))
            lai = pygame.image.load('data/Лэйхо.png')
            image2 = pygame.transform.scale(lai, (200, 200))
            screen.blit(image2, (800, 350))
            for i in self.list_point_menu_hero:
                if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                    point = i[5]
                    break
                else:
                    point = -1
            render(screen, self.font_menu, point, self.list_point_menu_hero)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_RIGHT:
                        if point < len(self.list_point_menu_hero) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        self.menu_level('Рифжих')
                    elif point == 2:
                        self.menu_level('Лэйхо')
                    elif point == 1:
                        run_hero = False
                    screen.fill(BACKGROUND_COLOR)
                    render(screen, self.font_menu, point, self.list_point_menu_hero)
            pygame.display.flip()

    def menu_level(self, hero):
        screen.fill(BACKGROUND_COLOR)
        run_level = True
        level = ""
        point = -1
        while run_level:
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            for i in self.list_point_menu_level:
                if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                    point = i[5]
                    break
                else:
                    point = -1
            render(screen, self.font_menu, point, self.list_point_menu_level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_RIGHT:
                        if point < len(self.list_point_menu_level) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 4:
                        run_level = False
                    else:
                        pygame.mixer.music.load(self.music)
                        pygame.mixer.music.set_volume(self.game_volume)
                        pygame.mixer.music.play(-1, 2)
                        if point == 0:
                            level = '1'
                        elif point == 1:
                            level = '2'
                        elif point == 2:
                            level = '3'
                        elif point == 3:
                            level = '4'
                        main_game(level, hero)
                        pygame.mixer.music.load('data/menu_music.mp3')
                        pygame.mixer.music.set_volume(self.menu_vol)
                        pygame.mixer.music.play()
                        screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()

    def menu(self):
        run = True

        point = -1
        pygame.mixer.music.load('data/menu_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        while run:
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            for i in self.list_point_main_menu:
                if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                    point = i[5]
                    break
                else:
                    point = -1
            render(screen, self.font_menu, point, self.list_point_main_menu)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_DOWN:
                        if point < len(self.list_point_main_menu) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        self.menu_hero()
                    elif point == 1:
                        self.menu_volume()
                    elif point == 3:
                        sys.exit()
                    elif point == 4:
                        pass
                    render(screen, self.font_menu, point, self.list_point_main_menu)
            pygame.display.flip()


game = Menu()
game.menu()
