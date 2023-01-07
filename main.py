import math
import random

import pygame

BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
WIDTH = 1200
HEIGHT = 800
FPS = 60


class Bullet:
    def __init__(self, mouse_coords, hero_pos, spread):
        self.is_died = False
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
    def __init__(self, coords):
        self.is_died = False
        self.v = 100
        self.coords = coords
        self.color = RED
        self.size = 10
        self.radius = self.size
        x, y = self.coords
        self.rect = pygame.Rect(x, y, 2 * self.size, 2 * self.size)

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


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 1000)

    enemy_upgrade_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(enemy_upgrade_timer, 50000)

    enemy_list = []
    bullet_list = []
    main_hero = Hero(130)
    mouse_coord = (0, 0)
    running = True
    direction_x = ""
    direction_y = ""
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet_list.append(Bullet(event.pos, main_hero.coords, 0))
                print(bullet_list[0].coords, bullet_list[0].rect.x, bullet_list[0].rect.y)

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
        for bullet in bullet_list:
            pygame.draw.circle(screen, bullet.color, bullet.coords, bullet.size)
            bullet.move()
            if bullet.is_died:
                bullet_list.remove(bullet)
        for enemy in enemy_list:
            pygame.draw.circle(screen, enemy.color, enemy.coords, enemy.size)
            enemy.move(main_hero.coords)
            collide_with = enemy.rect.collidelist([i.rect for i in bullet_list])
            if collide_with != -1:
                bullet_list[collide_with].is_died = True
                enemy.is_died = True
            if enemy.is_died:
                enemy_list.remove(enemy)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
