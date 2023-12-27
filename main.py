import pygame
import sys
from PIL import Image

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
pygame.init()
background_image = pygame.image.load("data/BG/BG.png").convert()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    pygame.display.update()
    pygame.display.flip()
pygame.quit()
sys.exit()
