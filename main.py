import random
import pygame
import sys

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
    for count, i in enumerate(water_map):
        print(len(i))
        for count1, j in enumerate(i):
            if int(j) and int(j) != 17:
                tile = pygame.image.load(f'data/Tiles/{j}.png').convert()
                tile.set_colorkey((255, 255, 255))
                screen.blit(tile, (count1 * 128, count * 128))
            elif int(j):
                tile = pygame.image.load(f'data/Tiles/{j}.png').convert()
                tile.set_colorkey((255, 255, 255))
                screen.blit(tile, (count1 * 128, count * 128 + 29))
    for count, i in enumerate(level):
        for count1, j in enumerate(i):
            if int(j):
                tile = pygame.image.load(f'data/Tiles/{j}.png').convert()
                tile.set_colorkey((255, 255, 255))
                screen.blit(tile, (count1 * 128, count * 128))
    return screen


class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        coords_list = []
        for col in range(61):
            for row in range(7):
                if int(level[row][col]) != 0 and int(level[row][col]) != 17 and int(level[row][col]) != 18 and int(
                        level[row - 1][col]) == 0:
                    coords_list.append((col, row - 1))
        self.xtile, self.ytile = random.choice(coords_list)
        print(self.xtile, self.ytile)

    def render(self):
        pass


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
background_image = pygame.image.load("data/BG/BG.png").convert()
running = True
level, water_map = load_level('FrozenValleys')
Player(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    screen = render_level(level, water_map, 'FrozenValleys', screen)
    pygame.display.update()
    pygame.display.flip()
pygame.quit()
sys.exit()
