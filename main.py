import pygame
import sys

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((800, 600))
pygame.init()
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_cir = (66, 170, 255)
        self.active_cir = (0, 191, 255)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_cir, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.music.load('menu_btn.mp3')
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play()
                pygame.time.delay(300)
                if action == quit:
                    pygame.quit()
                    quit()
        else:
            pygame.draw.rect(screen, self.inactive_cir, (x, y, self.width, self.height))
