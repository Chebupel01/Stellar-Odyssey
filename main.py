import random
import pygame
import sys
import warnings

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)
all_sprites = pygame.sprite.Group()


def load_level(level_name):
    level, water_map = [], []
    with open(f'data/Levels/{level_name}.txt', 'r', encoding='UTF-8') as file:
        for count, line in enumerate(file):
            for count1, i in enumerate(line.split('|')):
                path = f'data/{level_name}/Tiles/{i.strip()}.png'
                if '0' not in path:
                    all_sprites.add(Tile(128 * count1, 128 * count, path))
        '''with open(f'data/Levels/{level_name}Water.txt', 'r', encoding='UTF-8') as file1:
            for line in file1:
                water_map.append(line.split('|'))
        return level, water_map'''


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


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x + 64, y + 64))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xtile, self.ytile = 2, 2
        self.displacement = 64
        self.ydisplacement = 64
        self.player = pygame.image.load(f'data/FrozenValleys/snowman/снеговик.png').convert_alpha()
        self.rect = self.player.get_rect(midbottom=(int(self.displacement + 165 / 2), int(self.ydisplacement + 156)))
        self.direction = 'Right'
        self.now_direction = 'Right'
        self.jumping = False
        self.jump_time = 1

    def render(self, screen):
        if self.direction != self.now_direction:
            self.player = pygame.transform.flip(self.player, True, False)
            self.now_direction = self.direction
        if 896 <= self.displacement <= 7168:
            screen.blit(self.player, (896, self.ydisplacement))
        else:
            screen.blit(self.player, (self.displacement, self.ydisplacement))
        return screen

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.displacement -= 8
            self.direction = 'Left'
            for tile in all_sprites:
                if 896 <= self.displacement <= 7168:
                    tile.rect.x += 8
        if keys[pygame.K_d]:
            self.displacement += 8
            self.direction = 'Right'
            for tile in all_sprites:
                if 896 <= self.displacement <= 7168:
                    tile.rect.x -= 8
        if not self.jumping:
            if keys[pygame.K_SPACE]:
                self.jumping = True
        else:
            if self.jump_time <= 20:
                self.ydisplacement -= 16
            else:
                self.ydisplacement += 16
            if pygame.sprite.spritecollide(player, all_sprites, False) and self.jumping and self.jump_time > 20:
                self.jump_time = 0
                self.jumping = False
            self.jump_time += 1

    def collidePlayer(self):
        self.rect = self.player.get_rect(midbottom=(int(self.displacement + 165 / 2), int(self.ydisplacement + 156)))
        if not pygame.sprite.spritecollide(player, all_sprites, False) and not self.jumping and self.jump_time <= 20:
            self.jumping = True
            self.jump_time = 21
            print('Нет коллизии')




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
background_image = pygame.image.load("data/FrozenValleys/BG/BG.png").convert()
running = True
clock = pygame.time.Clock()
load_level('FrozenValleys')
player = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    player.move()
    collided_sprites = pygame.sprite.spritecollide(player, all_sprites, False)
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    player.collidePlayer()
    screen = player.render(screen)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
