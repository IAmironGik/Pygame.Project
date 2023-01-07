import pygame
import random
import sys


BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
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
            screen.fill(BLACK)
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if point == 0:
                        run = False
                    elif point == 2:
                        sys.exit()
            pygame.display.flip()

class Bullet:
    def __init__(self):
        self.is_died = False
        self.coords = WIDTH // 2, HEIGHT // 2
        self.color = WHITE
        self.size = 3
        self.v = 100


class Weapon:
    pass


class Enemy:
    def __init__(self, coords):
        self.is_died = False
        self.v = 100
        self.coords = coords
        self.color = RED
        self.size = 10

    def move(self, player_coords):
        x, y = self.coords
        xm, ym = player_coords
        k = ((x - xm) ** 2 + (y - ym) ** 2) ** 0.5
        vx = self.v * (xm - x) / k
        x += vx / FPS
        vy = self.v * (ym - y) / k
        y += vy / FPS
        self.coords = x, y
        if abs(xm - x) < 2 and abs(ym - y) < 2:
            self.is_died = True


class Hero:
    def __init__(self):
        self.is_died = False
        self.coords = WIDTH // 2, HEIGHT // 2
        self.color = WHITE
        self.size = 10
        self.v = 100

    def move(self, dx, dy):
        x, y = self.coords
        v = self.v
        if dy and dx:
            v = (self.v ** 2 / 2) ** 0.5
        if dy == "w":
            y -= v / FPS
        elif dy == "s":
            y += v / FPS
        if dx == "a":
            x -= v / FPS
        elif dx == "d":
            x += v / FPS
        self.coords = x, y


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 1000)

    enemy_list = []
    main_hero = Hero()
    mouse_coord = (0, 0)
    running = True
    direction_x = ""
    direction_y = ""
    list_points = [(500, 140, 'Играть', (0, 0, 255), (0, 255, 0), 0),
                   (500, 240, 'Настройки', (0, 0, 255), (0, 255, 0), 1),
                   (500, 340, 'Выход', (0, 0, 255), (0, 255, 0), 2)]
    game = Menu(list_points)
    game.menu()
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == enemy_spawn_timer:
                side = random.randint(0, 3)
                if side == 0:
                    x = random.randint(10, WIDTH - 10)
                    y = 10
                elif side == 1:
                    y = random.randint(10, HEIGHT - 10)
                    x = 10
                elif side == 2:
                    x = random.randint(10, WIDTH - 10)
                    y = HEIGHT - 10
                else:
                    y = random.randint(10, HEIGHT - 10)
                    x = 10
                enemy_list.append(Enemy((x, y)))
            key_events = pygame.key.get_pressed()
            if key_events:
                if key_events[pygame.K_a] and key_events[pygame.K_d]:
                    direction_x = ""
                elif key_events[pygame.K_a]:
                    direction_x = "a"
                elif key_events[pygame.K_d]:
                    direction_x = "d"
                else:
                    direction_x = ""
                if key_events[pygame.K_w] and key_events[pygame.K_s]:
                    direction_y = ""
                elif key_events[pygame.K_w]:
                    direction_y = "w"
                elif key_events[pygame.K_s]:
                    direction_y = "s"
                else:
                    direction_y = ""

        main_hero.move(direction_x, direction_y)
        pygame.draw.circle(screen, main_hero.color, main_hero.coords, main_hero.size)
        for enemy in enemy_list:
            pygame.draw.circle(screen, enemy.color, enemy.coords, enemy.size)
            enemy.move(main_hero.coords)
            if enemy.is_died:
                enemy_list.remove(enemy)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()