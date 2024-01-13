import pygame

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.init()
pygame.font.init()


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
    # основной цикл игры


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
show_menu()

class Snow():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.distance = 0
        self.snow_image = pygame.image.load('data/snowman/снег1.png')

    def move(self):
        self.x += self.speed
        self.distance += abs(self.speed)

    def get_current_image(self):
        return pygame.transform.scale(self.snow_image, (80, 80))


class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.start = x
        self.end = SCREEN_WIDTH - 200
        self.last_shoot_time = pygame.time.get_ticks()
        self.left_attack = [
            pygame.image.load('data/snowman/атакаслева1.png'),
            pygame.image.load('data/snowman/атакасл2.png'),
            pygame.image.load('data/snowman/атакасл3.png'),
            pygame.image.load('data/snowman/атакасл4.png'),
            pygame.image.load('data/snowman/атакасл5.png'),
            pygame.image.load('data/snowman/атакасл6.png'),
            pygame.image.load('data/snowman/атакасл7.png'),
            pygame.image.load('data/snowman/атакасл8.png'),
            pygame.image.load('data/snowman/атакасл9.png'),
            pygame.image.load('data/snowman/атакасл10.png')
        ]
        self.right_attack = [
            pygame.image.load('data/snowman/атака1.png'),
            pygame.image.load('data/snowman/атака2.png'),
            pygame.image.load('data/snowman/атака3.png'),
            pygame.image.load('data/snowman/атака4.png'),
            pygame.image.load('data/snowman/атака5.png'),
            pygame.image.load('data/snowman/атака6.png'),
            pygame.image.load('data/snowman/атака7.png'),
            pygame.image.load('data/snowman/атака8.png'),
            pygame.image.load('data/snowman/атака9.png'),
            pygame.image.load('data/snowman/атака10.png')
        ]
        self.enemy_image = pygame.image.load('data/snowman/снеговик.png')
        self.attack_duration = 1000
        self.attack_start_time = 0
        self.is_attacking = False
        self.attack_index = 0
        self.animation_speed = 70

    def move(self):
        current_time = pygame.time.get_ticks()
        time_since_last_shoot = current_time - self.last_shoot_time
        if time_since_last_shoot >= self.attack_duration and not self.is_attacking:
            self.is_attacking = True
            self.attack_start_time = current_time
            pygame.mixer.music.load('data/music/s2.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
        if self.is_attacking:
            time_since_attack_start = current_time - self.attack_start_time
            if time_since_attack_start >= self.animation_speed:
                if self.speed > 0:
                    self.enemy_image = self.right_attack[self.attack_index]
                    self.attack_index = (self.attack_index + 1) % len(self.right_attack)
                else:
                    self.enemy_image = self.left_attack[self.attack_index]
                    self.attack_index = (self.attack_index + 1) % len(self.left_attack)
                self.attack_start_time = current_time
            if time_since_last_shoot >= self.attack_duration + (len(self.left_attack) * self.animation_speed):
                self.is_attacking = False
                self.attack_index = 0
                self.last_shoot_time = current_time
                snow_speed = self.speed * 2
                if self.speed < 0:
                    snow_x = self.x - 80
                else:
                    snow_x = self.x + 200
                snow_y = self.y
                snow = Snow(snow_x, snow_y, snow_speed)
                snow_list.append(snow)
        else:
            if self.speed < 0:
                if self.x > self.start - self.speed:
                    self.x += self.speed
                else:
                    self.speed *= -1
                    self.x += self.speed
                self.enemy_image = pygame.image.load('data/snowman/снеговик2.png')
            else:
                if self.x < self.end + self.speed:
                    self.x += self.speed
                else:
                    self.speed *= -1
                    self.x += self.speed
                self.enemy_image = pygame.image.load('data/snowman/снеговик.png')


    def get_current_image(self):
        return pygame.transform.scale(self.enemy_image, (200, 200))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stellar Odyssey")
mucus = Enemy(0, 500)
mucus2 = Enemy(400, 500)
background_image = pygame.image.load("data/BG/BG.png").convert()
snow_list = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    mucus.move()
    mucus2.move()
    screen.blit(mucus.get_current_image(), (mucus.x, mucus.y))
    screen.blit(mucus2.get_current_image(), (mucus2.x, mucus2.y))
    for snow in snow_list:
        snow.move()
        screen.blit(snow.get_current_image(), (snow.x, snow.y))
        if snow.distance >= 350:
            snow_list.remove(snow)
        elif snow.x < 0 or snow.x > SCREEN_WIDTH:
            snow_list.remove(snow)
    pygame.display.update()
    clock.tick(30)
pygame.quit()