import random
import pygame
import sys
import warnings

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)


def load_level(level_name):
    level, water_map = [], []
    with open(f'data/Levels/{level_name}.txt', 'r', encoding='UTF-8') as file:
        for line in file:
            level.append(line.split('|'))
        with open(f'data/Levels/{level_name}Water.txt', 'r', encoding='UTF-8') as file1:
            for line in file1:
                water_map.append(line.split('|'))
        return level, water_map


def render_level(level, water_map, level_name, screen):
    minim, maxim = (0, 15) if player.xtile < 8 else ((45, 61)
                        if 53 < player.xtile else (player.xtile - 8, player.xtile + 8))
    for count, i in enumerate(water_map):
        for count1, j in enumerate(i[minim:maxim]):
            if count < 5:
                break
            if int(j) and int(j) != 17:
                tile = pygame.image.load(f'data/{level_name}/Tiles/{j.strip()}.png').convert()
                tile.set_colorkey((255, 255, 255))
                if player.xtile < 8 or 53 < player.xtile:
                    screen.blit(tile, (count1 * 128, count * 128))
                else:
                    screen.blit(tile, (count1 * 128 - player.displacement, count * 128))
            elif int(j):
                tile = pygame.image.load(f'data/{level_name}/Tiles/{j.strip()}.png').convert()
                tile.set_colorkey((255, 255, 255))
                if player.xtile < 8 or 53 < player.xtile:
                    screen.blit(tile, (count1 * 128, count * 128 + 29))
                else:
                    screen.blit(tile, (count1 * 128 - player.displacement, count * 128 + 29))
    for count, i in enumerate(level):
        for count1, j in enumerate(i[minim:maxim]):
            if int(j):
                tile = pygame.image.load(f'data/{level_name}/Tiles/{j.strip()}.png').convert()
                tile.set_colorkey((255, 255, 255))
                if player.xtile < 8 or 53 < player.xtile:
                    screen.blit(tile, (count1 * 128, count * 128))
                else:
                    screen.blit(tile, (count1 * 128 - player.displacement, count * 128))
    return screen


class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.xtile, self.ytile = 2, 2
        self.displacement = 64
        self.player = pygame.image.load(f'data/FrozenValleys/snowman/снеговик.png').convert_alpha()
        self.direction = 'Right'
        self.now_direction = 'Right'
        self.level = level

    def render(self, screen):
        self.player = self.player.get_rect(bottom=(100, 300))
        if self.direction != self.now_direction:
            self.player = pygame.transform.flip(self.player, True, False)
            self.now_direction = self.direction
        if self.displacement >= 64 and self.xtile == 7:
            screen.blit(self.player, (7 * 128 + self.displacement, self.ytile * 128))
            print((7, self.displacement))
        elif self.displacement >= 64 and self.xtile == 53:
            screen.blit(self.player, (7 * 128 + self.displacement, self.ytile * 128))
        elif self.xtile < 8:
            screen.blit(self.player, (self.xtile * 128 + self.displacement, self.ytile * 128))
        elif 53 < self.xtile:
            screen.blit(self.player, ((self.xtile - 45) * 128 + self.displacement, self.ytile * 128))
        else:
            screen.blit(self.player, (7 * 128 + 64, self.ytile * 128))
        return screen

    def move(self, command):
        if command == 'A':
            self.displacement -= 16
            self.direction = 'Left'
        if command == 'D':
            self.displacement += 16
            self.direction = 'Right'
        self.displacement, self.xtile = (self.displacement + 128, self.xtile - 1) if self.displacement < 0\
            else ((self.displacement - 128, self.xtile + 1) if self.displacement > 128 else (self.displacement, self.xtile))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
background_image = pygame.image.load("data/FrozenValleys/BG/BG.png").convert()
running = True
clock = pygame.time.Clock()
level, water_map = load_level('FrozenValleys')
player = Player(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move('D')
        if keys[pygame.K_a]:
            player.move('A')
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    screen = render_level(level, water_map, 'FrozenValleys', screen)
    screen = player.render(screen)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(300)
pygame.quit()
sys.exit()
