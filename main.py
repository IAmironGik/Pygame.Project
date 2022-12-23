import pygame
import random


BLACK = "#000000"
WHITE = "#FFFFFF"
WIDTH = 1200
HEIGHT = 800
FPS = 60


class Enemy:
    def __init__(self, coords):
        self.is_died = False
        self.v = 100
        self.coords = coords
        self.color = WHITE
        self.size = 10

    def move(self, mouse_coords):
        x, y = self.coords
        xm, ym = mouse_coords
        k = ((x - xm) ** 2 + (y - ym) ** 2) ** 0.5
        vx = self.v * (xm - x) / k
        x += vx / FPS
        vy = self.v * (ym - y) / k
        y += vy / FPS
        self.coords = x, y
        if abs(xm - x) < 2 and abs(ym - y) < 2:
            self.is_died = True


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 1000)

    enemy_list = []

    mouse_coord = (0, 0)
    running = True
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
            if event.type == pygame.MOUSEMOTION:
                mouse_coord = event.pos

        for enemy in enemy_list:
            pygame.draw.circle(screen, enemy.color, enemy.coords, enemy.size)
            enemy.move(mouse_coord)
            if enemy.is_died:
                enemy_list.remove(enemy)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()