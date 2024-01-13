import pygame
import sys

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((800, 600))
pygame.init()


def show_menu():
    menu_bc = pygame.image.load('data/BG/меню.png')
    start_btn = Button(288, 70)
    quit_btn = Button(120, 70)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bc, (0, 0))
        start_btn.draw(270, 200, 'Start game', start_game(), 50)
        quit_btn.draw(358, 300, 'quit', quit, 50)
        pygame.display.update()
        clock.tick(60)


def start_game():
    pass
    # основной цикл


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
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


pygame.font.init()
show_menu()