import math
import random
import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
GRAY = (150, 150, 150)
bullet_list = []


class Bullet:
    def __init__(self, mouse_coords, hero_pos, spread):
        self.is_died = False
        self.damage = 10
        self.color = WHITE
        self.coords = hero_pos
        self.size = 5
        self.v = 150

        x, y = self.coords
        distance_x = mouse_coords[0] - hero_pos[0]
        distance_y = mouse_coords[1] - hero_pos[1]

        angle = math.atan2(distance_y, distance_x) + spread

        self.vx = (self.v * math.cos(angle)) / FPS
        self.vy = (self.v * math.sin(angle)) / FPS
        self.rect = pygame.Rect(x, y, 2 * self.size, 2 * self.size)

    def move(self):
        x, y = self.coords
        x += self.vx
        y += self.vy
        self.coords = x, y
        if not 0 <= x <= WIDTH or not 0 <= y <= HEIGHT:
            self.is_died = True
        self.rect = pygame.Rect(x, y, 2 * self.size, 2 * self.size)


class Enemy:
    def __init__(self, coords, health, speed):
        self.is_died = False
        self.v = speed
        self.health = health
        self.coords = coords
        self.color = RED
        self.size = 10
        self.radius = self.size
        x, y = self.coords
        self.rect = pygame.Rect(x, y, 2 * self.size, 2 * self.size)

    def update(self):
        collide_with = self.rect.collidelist([i.rect for i in bullet_list])
        if collide_with != -1:
            bull = bullet_list[collide_with]
            bullet_list.pop(collide_with)
            self.health -= bull.damage
            if self.health <= 0:
                self.is_died = True

    def move(self, player_coords):
        x, y = self.coords
        xm, ym = player_coords
        k = ((x - xm) ** 2 + (y - ym) ** 2) ** 0.5
        vx = self.v * (xm - x) / k
        x += vx / FPS
        vy = self.v * (ym - y) / k
        y += vy / FPS
        self.coords = x, y
        self.rect = pygame.Rect(x, y, 2 * self.size, 2 * self.size)


class Hero:
    def __init__(self, speed):
        self.is_died = False
        self.coords = WIDTH // 2, HEIGHT // 2
        self.color = WHITE
        self.size = 10
        self.v = speed

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


def render(screen, font, number, list_points):
    for i in list_points:
        if number == i[5]:
            screen.blit(font.render(i[2], False, i[4]), (i[0], i[1]))
        else:
            screen.blit(font.render(i[2], False, i[3]), (i[0], i[1]))


def menu_stop(screen):
    pygame.mixer.music.pause()
    screen.fill(BLACK)
    pause = True
    font_menu = pygame.font.Font(None, 50)
    list_points = [(800, 600, 'Продолжить', RED, GRAY, 5),
                   (250, 600, 'Выйти в меню', RED, GRAY, 4),
                   (600, 100, '+хп', RED, GRAY, 0),
                   (600, 200, '+урон', RED, GRAY, 1),
                   (600, 300, 'Тройной выстрел', RED, GRAY, 2),
                   (600, 400, '-скорость врагов', RED, GRAY, 3)]
    point = 0
    while pause:
        pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
        x, y = pygame.mouse.get_pos()
        text_upgtate_1 = font_menu.render("Постоянные улучшения:", False, (255, 0, 0))
        screen.blit(text_upgtate_1, (80, 100))
        text_upgtate_2 = font_menu.render("Непостоянные улучшения:", False, (255, 0, 0))
        screen.blit(text_upgtate_2, (80, 300))
        for i in list_points:
            if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                point = i[5]
        render(screen, font_menu, point, list_points)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if point > 0:
                        point -= 1
                if event.key == pygame.K_DOWN:
                    if point < len(list_points) - 1:
                        point += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.mixer.music.unpause()
                if point == 4:
                    return True
                elif point == 5:
                    return False
        pygame.display.flip()


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 1000)

    enemy_upgrade_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(enemy_upgrade_timer, 50000)

    enemy_list = []
    main_hero = Hero(130)
    mouse_coord = (0, 0)

    killed_enemy = 0
    enemy_health = 30
    enemy_speed = 100

    direction_x = ""
    direction_y = ""
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_stop(screen):
                        running = False
                        bullet_list.clear()
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet_list.append(Bullet(event.pos, main_hero.coords, 0))

            if event.type == enemy_upgrade_timer:
                pygame.time.set_timer(enemy_spawn_timer, 500)

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
                enemy_list.append(Enemy((x, y), enemy_health, enemy_speed))
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
        if not running:
            break
        main_hero.move(direction_x, direction_y)
        pygame.draw.circle(screen, main_hero.color, main_hero.coords, main_hero.size)

        for index, bullet in enumerate(bullet_list):
            pygame.draw.circle(screen, bullet.color, bullet.coords, bullet.size)
            bullet.move()
            if bullet.is_died:
                bullet_list.pop(index)

        for enemy in enemy_list:
            pygame.draw.circle(screen, enemy.color, enemy.coords, enemy.size)
            enemy.move(main_hero.coords)
            enemy.update()
            if enemy.is_died:
                enemy_list.remove(enemy)
                killed_enemy += 1
                # if killed_enemy == 20:
                #     killed_enemy = 0
                #     enemy_health += 10
        pygame.display.flip()
        clock.tick(FPS)
