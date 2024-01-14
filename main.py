from random import randint, choice
import pygame
import sys


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
                if '0.png' not in path:
                    all_sprites.add(Tile(128 * count1, 128 * count, path))
                elif '10.png' in path:
                    all_sprites.add(Tile(128 * count1, 128 * count, path))
        '''with open(f'data/Levels/{level_name}Water.txt', 'r', encoding='UTF-8') as file1:
            for line in file1:
                water_map.append(line.split('|'))
        return level, water_map'''


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x + 64, y + 64))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xtile, self.ytile = 2, 2
        self.displacement = 70
        self.ydisplacement = 112
        self.displacement_on_display = 64
        self.player = pygame.image.load(f'hero/11.png').convert_alpha()
        self.rect = self.player.get_rect(midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                                                    int(self.ydisplacement + self.player.get_height())))
        self.direction = 'Right'
        self.now_direction = 'Right'
        self.jumping = False
        self.running = False
        self.jump_time = 1
        self.run_time = 0
        self.running_animation = ['81.png', '82.png', '83.png', '84.png', '85.png', '86.png', '87.png', '88.png',
                                  '89.png', '810.png', '811.png', '812.png', '813.png', '814.png', '815.png']
        self.jumping_animation = ['21.png', '22.png', '23.png', '24.png', '25.png', '26.png']

    def render(self, screen):
        self.now_direction = 'Right'
        if self.jumping:
            if self.jump_time <= 5:
                image_name = self.jumping_animation[0]
            elif self.jump_time <= 10:
                image_name = self.jumping_animation[1]
            elif self.jump_time <= 20:
                image_name = self.jumping_animation[2]
            elif self.jump_time <= 25:
                image_name = self.jumping_animation[3]
            elif self.jump_time <= 30:
                image_name = self.jumping_animation[4]
            elif self.jump_time <= 200:
                image_name = self.jumping_animation[5]
            if self.direction != self.now_direction:
                self.player = pygame.transform.flip(pygame.image.load(f'hero/{image_name}').convert_alpha(), True, False)
            else:
                self.player = pygame.image.load(f'hero/{image_name}').convert_alpha()
        elif self.run_time % 5 == 0 and self.running:
            if self.run_time >= 75:
                self.run_time = 0
            if self.direction != self.now_direction:
                self.now_direction = self.direction
                self.player = pygame.transform.flip(
                    pygame.image.load(f'hero/{self.running_animation[self.run_time // 5]}').convert_alpha(), True,
                    False)
            else:
                self.player = pygame.image.load(f'hero/{self.running_animation[self.run_time // 5]}').convert_alpha()
        elif not self.running and not self.jumping:
            if self.direction != self.now_direction:
                self.player = pygame.transform.flip(pygame.image.load(f'hero/11.png').convert_alpha(), True, False)
            else:
                self.player = pygame.image.load(f'hero/11.png').convert_alpha()

        if 896 <= self.displacement <= 7168:
            self.displacement_on_display = 896
            screen.blit(self.player, (self.displacement_on_display, self.ydisplacement))
        elif 896 > self.displacement:
            self.displacement_on_display = self.displacement
            screen.blit(self.player, (self.displacement_on_display, self.ydisplacement))
        else:
            self.displacement_on_display = 896 - self.displacement + 7168
            screen.blit(self.player, (self.displacement_on_display, self.ydisplacement))
        self.running = False
        return screen

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.displacement -= 8
            self.direction = 'Left'
            if 896 <= self.displacement <= 7168:
                for tile in all_sprites:
                    tile.rect.x += 8
            self.run_time += 1
            self.running = True
        if keys[pygame.K_d]:
            self.displacement += 8
            self.direction = 'Right'
            if 896 <= self.displacement <= 7168:
                for tile in all_sprites:
                    tile.rect.x -= 8
            self.run_time += 1
            self.running = True
        if not keys:
            self.running = False
            self.run_time = 0
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
        self.rect = self.player.get_rect(midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                                                    int(self.ydisplacement + self.player.get_height())))
        if not pygame.sprite.spritecollide(player, all_sprites, False) and not self.jumping and self.jump_time <= 20:
            self.jumping = True
            self.jump_time = 21
        if pygame.sprite.spritecollide(player, all_sprites, False):
            print('Нет коллизии')
            for tile in all_sprites:
                collision_rect = player.rect.clip(tile.rect)
            print(f"Коллизия произошла в области: {collision_rect}")


class SnowParticles:
    def __init__(self):
        self.snowflakes = []
        for i in range(0, 1800, 2):
            for j in range(randint(0, 10)):
                self.snowflakes.append([i, randint(0, 1800)])

    def render(self, screen):
        for i in range(randint(0, 10)):
            self.snowflakes.append([randint(0, 1800), 0])
        for count, i in enumerate(self.snowflakes):
            pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], 4, 4))
            if choice(['RIGHT', 'LEFT']) == 'RIGHT':
                self.snowflakes[count][0] += 4
            else:
                self.snowflakes[count][0] -= 4
            self.snowflakes[count][1] += 2
            if self.snowflakes[count][1] > 893:
                self.snowflakes.pop(count)

        return screen



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
background_image = pygame.image.load("data/FrozenValleys/BG/BG.png").convert()
running = True
clock = pygame.time.Clock()
load_level('FrozenValleys')
player = Player()
particles = SnowParticles()
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
