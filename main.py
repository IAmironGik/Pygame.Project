import math
import os
import random
import sys

import pygame


BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60
GRAY = (150, 150, 150)
bullet_list = []


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


class Bullet:
    def __init__(self, mouse_coords, hero_pos, spread=0):
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


class Enemy(pygame.sprite.Sprite):

    def __init__(self, group, coords, health, speed):
        super().__init__(group)

        self.image = load_image("Рифжих.png")
        self.rect = self.image.get_rect()
        self.coords = coords
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.is_died = False
        self.v = speed
        self.health = health

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
        self.rect.x = x
        self.rect.y = y


class Hero(pygame.sprite.Sprite):
    def __init__(self, group, speed, image, health):
        super().__init__(group)

        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.coords = WIDTH // 2, HEIGHT // 2
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2

        self.health = health
        self.v = speed

    def move(self, dx, dy):
        x, y = self.coords
        v = self.v
        if dy and dx:
            v = (self.v ** 2 / 2) ** 0.5
        y += (v / FPS) * dy
        x += (v / FPS) * dx

        self.coords = x, y
        self.rect.x = x
        self.rect.y = y


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
                   (600, 300, 'тройной выстрел', RED, GRAY, 2),
                   (600, 400, 'замедлить врагов', RED, GRAY, 3)]

    point = -1
    while pause:
        pygame.draw.rect(screen, RED, (70, 50, 1070, 700), 1)
        x, y = pygame.mouse.get_pos()

        heart = pygame.image.load('data/сердце.png')
        image1 = pygame.transform.scale(heart, (50, 50))
        screen.blit(image1, (700, 100))

        weap = pygame.image.load('data/дробовик.png')
        image2 = pygame.transform.scale(weap, (50, 50))
        screen.blit(image2, (900, 300))

        damage = pygame.image.load('data/урон.png')
        image3 = pygame.transform.scale(damage, (50, 50))
        screen.blit(image3, (720, 200))

        speed = pygame.image.load('data/перо.png')
        image4 = pygame.transform.scale(speed, (50, 50))
        screen.blit(image4, (900, 400))

        text_upgtate_1 = font_menu.render("Постоянные улучшения:", False, (255, 0, 0))
        screen.blit(text_upgtate_1, (80, 100))
        text_upgtate_2 = font_menu.render("Временные улучшения:", False, (255, 0, 0))
        screen.blit(text_upgtate_2, (80, 300))
        for i in list_points:
            if i[0] < x < (i[0] + 150) and i[1] < y < (i[1] + 50):
                point = i[5]
                break
            else:
                point = -1
        render(screen, font_menu, point, list_points)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if point > 0:
                        point -= 1
                if event.key == pygame.K_RIGHT:
                    if point < len(list_points) - 1:
                        point += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if point == 4:
                    pygame.mixer.music.unpause()
                    return True
                elif point == 5:
                    pygame.mixer.music.unpause()
                    return False
        pygame.display.flip()


def main_game():
    global bullet_list

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullet_list = []

    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 1000)

    enemy_upgrade_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(enemy_upgrade_timer, 50000)

    enemy_list = []
    main_hero = Hero(all_sprites, 130, "Лэйхо.png", 5)

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
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet_list.append(Bullet(event.pos, (main_hero.rect.x + main_hero.rect.w // 2,
                                                      main_hero.rect.y + main_hero.rect.h // 2)))

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
                enemy_list.append(Enemy(all_sprites, (x, y), enemy_health, enemy_speed))

            key_events = pygame.key.get_pressed()
            if key_events:
                if key_events[pygame.K_a] == key_events[pygame.K_d]:
                    direction_x = 0
                elif key_events[pygame.K_a]:
                    direction_x = -1
                elif key_events[pygame.K_d]:
                    direction_x = 1
                if key_events[pygame.K_w] == key_events[pygame.K_s]:
                    direction_y = 0
                elif key_events[pygame.K_w]:
                    direction_y = -1
                elif key_events[pygame.K_s]:
                    direction_y = 1

        main_hero.move(direction_x, direction_y)
        all_sprites.draw(screen)

        for index, bullet in enumerate(bullet_list):
            pygame.draw.circle(screen, bullet.color, bullet.coords, bullet.size)
            bullet.move()
            if bullet.is_died:
                bullet_list.pop(index)

        for enemy in enemy_list:
            enemy.move((main_hero.rect.x, main_hero.rect.y))

            enemy.update()
            if enemy.is_died:
                enemy.kill()
                enemy_list.remove(enemy)
                killed_enemy += 1

        pygame.display.flip()
        clock.tick(FPS)
