import pygame
import sys
from PIL import Image

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
r_image = pygame.image.load('data/snowman/снеговик.png')
l_image = pygame.image.load('data/snowman/снеговик2.png')

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

class enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.start = x
        self.end = SCREEN_WIDTH - 200

    def move(self):
        if self.speed < 0:
            if self.x > self.start - self.speed:
                self.x += self.speed
            else:
                self.speed *= -1
                self.x += self.speed
            self.enemy = pygame.transform.scale(l_image, (200, 200))
        else:
            if self.x < self.end + self.speed:
                self.x += self.speed
            else:
                self.speed *= -1
                self.x += self.speed
            self.enemy = pygame.transform.scale(r_image, (200, 200))




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
mucus = enemy(0, 500)
background_image = pygame.image.load("data/BG/BG.png").convert()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    mucus.move()
    screen.blit(mucus.enemy, (mucus.x, mucus.y))
    pygame.display.update()
    clock.tick(30)
    pygame.display.flip()
pygame.quit()
sys.exit()
