import pygame
import os
import random

pygame.init()
pygame.font.init()
START_MENU_WIDTH = 800
START_MENU_HEIGHT = 600
GAME_WIDTH = 1800
GAME_HEIGHT = 893
WHITE = (255, 255, 255)
pygame.display.set_caption('Stellar Odyssey')
clock = pygame.time.Clock()
start_menu_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))
end_menu_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))
win_menu_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))

game_screen = None
snow_list = []
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.image = pygame.image.load(path)
        if '14' in path or '15' in path or '16' in path:
            self.rect = self.image.get_rect(center=(x + 64, y + 32))
            self.rect.height = 64
        else:
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
                                                    int((self.ydisplacement + self.player.get_height() * 0.6))))
        self.direction = 'Right'
        self.now_direction = 'Right'
        self.jumping = False
        self.running = False
        self.attacking = False
        self.jump_time = 1
        self.run_time = 0
        self.attacking_time = 1
        self.running_animation = ['81.png', '82.png', '83.png', '84.png', '85.png', '86.png', '87.png', '88.png',
                                  '89.png', '810.png', '811.png', '812.png', '813.png', '814.png', '815.png']
        self.jumping_animation = ['21.png', '22.png', '23.png', '24.png', '25.png', '26.png']
        self.attack_animation = ['31.png', '32.png', '33.png', '34.png', '35.png', '36.png', '37.png']

    def render(self, screen):
        self.now_direction = 'Right'
        if self.attacking:
            if self.attacking_time <= 4:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 8:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 12:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 16:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 20:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 24:
                image_name = self.attack_animation[self.attacking // 4]
            elif self.attacking_time <= 28:
                image_name = self.attack_animation[self.attacking // 4]
                self.attacking_time = 1
                self.attacking = False
            if self.direction != self.now_direction:
                self.player = pygame.transform.flip(pygame.image.load(f'hero/{image_name}').convert_alpha(), True,
                                                    False)
            else:
                self.player = pygame.image.load(f'hero/{image_name}').convert_alpha()
            self.attacking_time += 1
        elif self.jumping:
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
                self.player = pygame.transform.flip(pygame.image.load(f'hero/{image_name}').convert_alpha(), True,
                                                    False)
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
        resized_image = pygame.transform.scale(self.player,
                                               (int(player.rect.width * 0.6), int(player.rect.height * 0.6)))
        if 896 <= self.displacement <= 7168:
            self.displacement_on_display = 896
            screen.blit(resized_image, (self.displacement_on_display, self.ydisplacement))
        elif 896 > self.displacement:
            self.displacement_on_display = self.displacement
            screen.blit(resized_image, (self.displacement_on_display, self.ydisplacement))
        else:
            self.displacement_on_display = 896 - self.displacement + 7168
            screen.blit(resized_image, (self.displacement_on_display, self.ydisplacement))
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
                                                    int((self.ydisplacement + self.player.get_height() * 0.6))))
        player.rect.width = int(self.player.get_width() * 0.75)
        if not pygame.sprite.spritecollide(player, all_sprites, False) and not self.jumping and self.jump_time <= 20:
            self.jumping = True
            self.jump_time = 21

    def attack(self):
        self.attacking = True


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

def win_game():
    """
    Функция для показа выигрыша
    """
    pygame.mixer.music.load('game-win.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    # создание заднего фона
    end_bc = pygame.image.load('data/BG/win.jpg')
    # Создаем кнопку "restart_btn"
    restart_btn = Button(190, 70, (68, 148, 74), (152, 251, 152), action=start_game)
    # Создаем кнопку "menu_btn"
    menu_btn = Button(130, 70, (68, 148, 74), (152, 251, 152), action=show_menu)
    show = True
    # Запускаем цикл
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Отображение заднего фона меню
        win_menu_screen.blit(end_bc, (0, 0))
        # Отображение кнопки "restart_btn"
        restart_btn.draw(310, 350, 'Restart', 50)
        # Отображение кнопки "menu_btn"
        menu_btn.draw(342, 450, 'Menu', 50)
        # Обновляем экрана
        pygame.display.update()
        clock.tick(60)


def end_game():
    """
    Функция для показа конца игры
    """
    pygame.mixer.music.load('zvuki_game_over.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    # создание заднего фона
    end_bc = pygame.image.load('data/BG/gameover.jpg')
    # Создаем кнопку "restart_btn"
    restart_btn = Button(190, 70, (190, 45, 48), (255, 0, 0), action=start_game)
    # Создаем кнопку "menu_btn"
    menu_btn = Button(130, 70, (190, 45, 48), (255, 0, 0), action=show_menu)
    show = True
    # Запускаем цикл
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Отображение заднего фона меню
        end_menu_screen.blit(end_bc, (0, 0))
        # Отображение кнопки "restart_btn"
        restart_btn.draw(310, 350, 'Restart', 50)
        # Отображение кнопки "menu_btn"
        menu_btn.draw(342, 450, 'Menu', 50)
        # Обновляем экрана
        pygame.display.update()
        clock.tick(60)


def show_menu():
    pygame.mixer.music.load('fonmusic.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    # создание заднего фона
    menu_bc = pygame.image.load('data/BG/меню.png')
    # Создаем кнопку "start_btn"
    start_btn = Button(288, 70, (66, 170, 255), (0, 191, 255), action=start_game)
    # Создаем кнопку "quit_btn"
    quit_btn = Button(120, 70, (66, 170, 255), (0, 191, 255), action=quit)
    show = True
    # Запускаем цикл
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Отображение заднего фона меню
        start_menu_screen.blit(menu_bc, (0, 0))
        # Отображение кнопки "start_btn"
        start_btn.draw(270, 200, 'Start game', 50)
        # Отображение кнопки "quit_btn"
        quit_btn.draw(358, 300, 'quit', 50)
        # Обновляем экрана
        pygame.display.update()
        clock.tick(60)


def start_game():
    """
    функция для запуска основного цикла
    """
    # создание списка для хранения координат снежинок
    snowsp = []
    for i in range(1200):
        x = random.randrange(0, GAME_WIDTH)
        y = random.randrange(0, GAME_HEIGHT)
        snowsp.append([x, y])
    # объявление глобальных переменных
    global game_screen, snow_list
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # создание экрана
    game_screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.mixer.init()
    mucus = Enemy(0, 500, 0, 1000)
    mucus2 = Enemy(400, 500, 0, 1000)
    # загрузка фона игры
    background_image = pygame.image.load("data/BG/BG.png").convert()
    snow_list = []
    running = True
    # основной игровой цикл
    while running:
        for event in pygame.event.get():
            # проверка на событие закрытия окна
            if event.type == pygame.QUIT:
                running = False
        game_screen.fill(WHITE)
        game_screen.blit(background_image, (0, 0))
        mucus.move()
        mucus2.move()
        game_screen.blit(mucus.get_current_image(), (mucus.x, mucus.y))
        game_screen.blit(mucus2.get_current_image(), (mucus2.x, mucus2.y))
        for i in range(len(snowsp)):
            pygame.draw.circle(game_screen, WHITE, snowsp[i], 2)
            snowsp[i][1] += 1
            if snowsp[i][1] > GAME_HEIGHT:
                y = random.randrange(-50, -10)
                snowsp[i][1] = y
                x = random.randrange(0, GAME_WIDTH)
                snowsp[i][0] = x
        for snow in snow_list:
            snow.move()
            game_screen.blit(snow.get_current_image(), (snow.x, snow.y))
            if snow.distance >= 350:
                snow_list.remove(snow)
            elif snow.x < 0 or snow.x > GAME_WIDTH:
                snow_list.remove(snow)
        # обновление экрана
        pygame.display.update()
        clock.tick(30)
    # завершение игры
    pygame.quit()


class Button:
    def __init__(self, width, height, inactive_cir, active_cir, action=None):
        self.width = width
        self.height = height
        self.inactive_cir = inactive_cir
        self.active_cir = active_cir
        self.action = action

    def draw(self, x, y, message, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(start_menu_screen, self.active_cir, (x, y, self.width, self.height))
            if click[0] == 1 and self.action:
                pygame.mixer.music.load('menu_btn.mp3')
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play()
                pygame.time.delay(300)
                self.action()
        else:
            pygame.draw.rect(start_menu_screen, self.inactive_cir, (x, y, self.width, self.height))
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    start_menu_screen.blit(text, (x, y))


class Snow:
    """
    класс снега
    """

    def __init__(self, x, y, speed):
        """
        Инициализия
        """
        self.x = x
        self.y = y
        # скорость движения снега
        self.speed = speed
        self.distance = 0
        self.snow_image = pygame.image.load('data/snowman/снег1.png')

    def move(self):
        # Изменяем позицию снега
        self.x += self.speed
        self.distance += abs(self.speed)

    def get_current_image(self):
        """
        Возвращение изображение снежинки
        """
        return pygame.transform.scale(self.snow_image, (80, 80))


class Enemy:
    """
    класс снега
    """

    def __init__(self, x, y, start, end):
        """
        Инициализация
        """
        self.x = x
        self.y = y
        self.speed = 8
        self.start = start
        self.end = end
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
        """
        Возвращение изображение врага
        """
        return pygame.transform.scale(self.enemy_image, (200, 200))