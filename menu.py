import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from main import main

BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
GRAY = (150, 150, 150)
pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


class Menu:
    def __init__(self, list_points):
        self.list_points = list_points
        self.game_volume = 0.5
        self.music = 'data/game_music_1'

    def render(self, screen, font, number):
        for i in self.list_points:
            if number == i[5]:
                screen.blit(font.render(i[2], False, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], False, i[3]), (i[0], i[1]))

    def menu_volume(self):
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
        slider_menu = Slider(screen, 500, 100, 500, 40, min=0, max=100, step=1,
                             initial=(pygame.mixer.music.get_volume()) * 100)
        box_menu = TextBox(screen, 1050, 100, 50, 50, fontSize=30)
        slider_game = Slider(screen, 500, 200, 500, 40, min=0, max=100, step=1, initial=self.game_volume * 100)
        box_game = TextBox(screen, 1050, 200, 50, 50, fontSize=30)
        box_menu.disable()
        box_game.disable()
        run_volume = True
        self.list_points = [(100, 600, 'Обратно в меню', RED, GRAY, 0),
                            (100, 400, 'Мелодия 1', RED, GRAY, 1),
                            (300, 400, 'Мелодия 2', RED, GRAY, 2),
                            (500, 400, 'Мелодия 3', RED, GRAY, 3)]
        self.render(screen, self.font_menu, 0)
        point = 0
        while run_volume:
            events = pygame.event.get()
            text_1 = self.font_menu.render("Громкость в меню", False, (255, 0, 0))
            screen.blit(text_1, (100, 100))
            text_2 = self.font_menu.render("Громкость в игре", False, (255, 0, 0))
            screen.blit(text_2, (100, 200))
            text_3 = self.font_menu.render("Выберите мелодию для проигрывания в игре", False, (255, 0, 0))
            screen.blit(text_3, (100, 300))
            x, y = pygame.mouse.get_pos()
            for i in self.list_points:
                if x > i[0] and x < (i[0] + 150) and y > i[1] and y < (i[1] + 50):
                    point = i[5]
            self.render(screen, self.font_menu, point)
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    elif event.key == pygame.K_RIGHT:
                        if point < len(self.list_points) - 1:
                            point += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        pygame.mixer.music.load('data/menu_music.mp3')
                        pygame.mixer.music.set_volume(slider_menu.getValue() / 100)
                        pygame.mixer.music.play(-1)
                        run_volume = False
                        screen.fill(BLACK)
                    else:
                        if not self.music == f'data/game_music_{point}.mp3':
                            self.music = f'data/game_music_{point}.mp3'
                            pygame.mixer.music.load(self.music)
                            pygame.mixer.music.set_volume(slider_game.getValue() / 100)
                            pygame.mixer.music.play(-1, 1)
            box_menu.setText(slider_menu.getValue())
            box_game.setText(slider_game.getValue())

            self.menu_vol = slider_menu.getValue() / 100
            self.game_volume = slider_game.getValue() / 100
            pygame.mixer.music.set_volume(self.menu_vol)

            pygame_widgets.update(events)
            pygame.display.update()
            pygame.display.flip()
        slider_menu.hide()
        slider_game.hide()
        box_menu.hide()
        box_game.hide()

    def menu_hero(self):
        screen.fill(BLACK)
        run_hero = True
        self.list_points = [(250, 600, 'Рифжих', RED, GRAY, 0),
                            (850, 600, 'Лэйхо', RED, GRAY, 2),
                            (500, 650, 'Назад', RED, GRAY, 1)]
        self.hero = ''
        point = 0
        while run_hero:
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            rif = pygame.image.load('data/Рифжих.jpg')
            image1 = pygame.transform.scale(rif, (200, 200))
            screen.blit(image1, (220, 350))
            lai = pygame.image.load('data/Лэйхо.jpg')
            image2 = pygame.transform.scale(lai, (200, 200))
            screen.blit(image2, (800, 350))
            for i in self.list_points:
                if x > i[0] and x < (i[0] + 150) and y > i[1] and y < (i[1] + 50):
                    point = i[5]
            self.render(screen, self.font_menu, point)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_RIGHT:
                        if point < len(self.list_points) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        self.hero = 'Рифжих'
                        self.menu_level()
                        screen.fill(BLACK)
                        self.list_points = [(250, 600, 'Рифжих', RED, GRAY, 0),
                                            (850, 600, 'Лэйхо', RED, GRAY, 2),
                                            (500, 650, 'Назад', RED, GRAY, 1)]
                        self.render(screen, self.font_menu, point)
                    elif point == 2:
                        self.hero = 'Лэйхо'
                        self.menu_level()
                        screen.fill(BLACK)
                        self.list_points = [(250, 600, 'Рифжих', RED, GRAY, 0),
                                            (850, 600, 'Лэйхо', RED, GRAY, 2),
                                            (500, 650, 'Назад', RED, GRAY, 1)]
                        self.render(screen, self.font_menu, point)
                    elif point == 1:
                        run_hero = False
            pygame.display.flip()

    def menu_level(self):
        screen.fill(BLACK)
        run_level = True
        self.list_points = [(150, 300, 'Уровень 1', RED, GRAY, 0),
                            (850, 300, 'Уровень 2', RED, GRAY, 1),
                            (150, 600, 'Уровень 3', RED, GRAY, 2),
                            (850, 600, 'Уровень 4', RED, GRAY, 3),
                            (500, 650, 'Назад', RED, GRAY, 4)]
        self.level = ''
        point = 0
        while run_level:
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            for i in self.list_points:
                if x > i[0] and x < (i[0] + 150) and y > i[1] and y < (i[1] + 50):
                    point = i[5]
            self.render(screen, self.font_menu, point)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_RIGHT:
                        if point < len(self.list_points) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 4:
                        run_level = False
                    else:
                        pygame.mixer.music.load(self.music)
                        pygame.mixer.music.set_volume(self.game_volume)
                        pygame.mixer.music.play(-1, 2)
                        if point == 0:
                            self.level = '1'
                        elif point == 1:
                            self.level = '2'
                        elif point == 2:
                            self.level = '3'
                        elif point == 3:
                            self.level = '4'
                        main()
                        pygame.mixer.music.load('data/menu_music.mp3')
                        pygame.mixer.music.set_volume(self.menu_vol)
                        pygame.mixer.music.play()
                        screen.fill(BLACK)
            pygame.display.flip()

    def menu(self):
        run = True
        self.font_menu = pygame.font.Font(None, 50)
        point = 0
        pygame.mixer.music.load('data/menu_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        while run:
            pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
            x, y = pygame.mouse.get_pos()
            for i in self.list_points:
                if x > i[0] and x < (i[0] + 150) and y > i[1] and y < (i[1] + 50):
                    point = i[5]
            self.render(screen, self.font_menu, point)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_DOWN:
                        if point < len(self.list_points) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        self.menu_hero()
                        screen.fill(BLACK)
                        self.list_points = [(500, 200, 'Играть', RED, GRAY, 0),
                                            (500, 300, 'Магазин', RED, GRAY, 1),
                                            (500, 400, 'Настройки', RED, GRAY, 2),
                                            (500, 500, 'Правила', RED, GRAY, 3),
                                            (500, 600, 'Выход', RED, GRAY, 4)]
                        self.render(screen, self.font_menu, point)
                    elif point == 2:
                        self.menu_volume()
                        screen.fill(BLACK)
                        self.list_points = [(500, 200, 'Играть', RED, GRAY, 0),
                                            (500, 300, 'Магазин', RED, GRAY, 1),
                                            (500, 400, 'Настройки', RED, GRAY, 2),
                                            (500, 500, 'Правила', RED, GRAY, 3),
                                            (500, 600, 'Выход', RED, GRAY, 4)]
                        self.render(screen, self.font_menu, point)
                    elif point == 4:
                        sys.exit()
            pygame.display.flip()


list_points = [(500, 200, 'Играть', RED, GRAY, 0),
               (500, 300, 'Магазин', RED, GRAY, 1),
               (500, 400, 'Настройки', RED, GRAY, 2),
               (500, 500, 'Правила', RED, GRAY, 3),
               (500, 600, 'Выход', RED, GRAY, 4)]
game = Menu(list_points)
game.menu()
