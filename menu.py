import pygame
import sys

BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


class Menu:
    def __init__(self, list_points=[600, 400, 'Игарть', (0, 0, 255), (0, 255, 0), 0]):
        self.list_points = list_points

    def render(self, screen, font, number):
        for i in self.list_points:
            if number == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        run = True
        font_menu = pygame.font.Font(None, 50)
        point = 0
        while run:
            bg = pygame.image.load("bg.jpg")
            screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for i in self.list_points:
                if x > i[0] and x < (i[0] + 150) and y > i[1] and y < (i[1] + 50):
                    point = i[5]
            self.render(screen, font_menu, point)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if point > 0:
                            point -= 1
                    if event.key == pygame.K_DOWN:
                        if point < len(self.list_points) - 1:
                            point += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        run = False
                    elif point == 3:
                        sys.exit()
            pygame.display.flip()
list_points = [(500, 240, 'Играть', (0, 0, 255), (0, 255, 0), 0),
               (500, 340, 'Настройки', (0, 0, 255), (0, 255, 0), 1),
               (500, 440, 'Об авторах', (0, 0, 255), (0, 255, 0), 2),
               (500, 540, 'Выход', (0, 0, 255), (0, 255, 0), 3)]
game = Menu(list_points)
game.menu()