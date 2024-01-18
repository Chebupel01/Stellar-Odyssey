import pygame
import os
import random
import sys
import pygame.freetype

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
Attacki = 0


def load_level(level_name):
    all_sprites = pygame.sprite.Group()
    with open(f'data/Levels/{level_name}.txt', 'r', encoding='UTF-8') as file:
        for count, line in enumerate(file):
            for count1, i in enumerate(line.split('|')):
                path = f'data/{level_name}/Tiles/{i.strip()}.png'
                if '0.png' not in path:
                    all_sprites.add(Tile(128 * count1, 128 * count, path))
                elif '10.png' in path:
                    all_sprites.add(Tile(128 * count1, 128 * count, path))
    return all_sprites


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
        self.displacement = 120
        self.ydisplacement = 220
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

    def render(self, screen, snowmans):
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
            if self.attacking_time <= 28:
                image_name = self.attack_animation[self.attacking // 4]
                self.attacking_time = 1
                self.attacking = False
                for count, snowman in enumerate(snowmans):
                    if pygame.sprite.collide_rect(player, snowman):
                        snowmans.pop(count)
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
        return screen, snowmans

    def move(self, all_sprites, snowmens):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.displacement -= 8
            self.direction = 'Left'
            if 896 <= self.displacement <= 7168:
                for tile in all_sprites:
                    tile.rect.x += 8
                for snowman in snowmens:
                    snowman.x += 8
            self.run_time += 1
            self.running = True
        if keys[pygame.K_d]:
            self.displacement += 8
            self.direction = 'Right'
            if 896 <= self.displacement <= 7168:
                for tile in all_sprites:
                    tile.rect.x -= 8
                for snowman in snowmens:
                    snowman.x -= 8
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
        return all_sprites

    def collidePlayer(self, all_sprites):
        self.rect = self.player.get_rect(midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                                                    int((self.ydisplacement + self.player.get_height() * 0.6))))
        player.rect.width = int(self.player.get_width() * 0.75)
        if not pygame.sprite.spritecollide(player, all_sprites, False) and not self.jumping and self.jump_time <= 20:
            self.jumping = True
            self.jump_time = 21
        return all_sprites

    def attack(self):
        global Attacki
        Attacki += 1
        self.attacking = True

    def game_over(self, running, game):
        status = ''
        if player.rect.y > 1000:
            running = False
            status = 'GAME OVER'
            self.displacement = 120
            self.ydisplacement = 220
            self.displacement_on_display = 64
            self.player = pygame.image.load(f'hero/11.png').convert_alpha()
            self.rect = self.player.get_rect(
                midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                           int((self.ydisplacement + self.player.get_height() * 0.6))))
            self.direction = 'Right'
            self.now_direction = 'Right'
            self.jumping = False
            self.running = False
            self.attacking = False
            self.jump_time = 1
            self.run_time = 0
            self.attacking_time = 1
        if game:
            running = False
            status = 'GAME OVER'
            self.displacement = 120
            self.ydisplacement = 220
            self.displacement_on_display = 64
            self.player = pygame.image.load(f'hero/11.png').convert_alpha()
            self.rect = self.player.get_rect(
                midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                           int((self.ydisplacement + self.player.get_height() * 0.6))))
            self.direction = 'Right'
            self.now_direction = 'Right'
            self.jumping = False
            self.running = False
            self.attacking = False
            self.jump_time = 1
            self.run_time = 0
            self.attacking_time = 1
        return running, status

    def win(self, running, game):
        status = ''
        if self.displacement > 7000:
            running = False
            status = 'WIN'
            self.displacement = 120
            self.ydisplacement = 220
            self.displacement_on_display = 64
            self.player = pygame.image.load(f'hero/11.png').convert_alpha()
            self.rect = self.player.get_rect(
                midbottom=(int(self.displacement_on_display + self.player.get_height() / 2),
                           int((self.ydisplacement + self.player.get_height() * 0.6))))
            self.direction = 'Right'
            self.now_direction = 'Right'
            self.jumping = False
            self.running = False
            self.attacking = False
            self.jump_time = 1
            self.run_time = 0
            self.attacking_time = 1
        return running, status


class SnowParticles:
    def __init__(self):
        self.snowflakes = []
        for i in range(0, 1800, 2):
            for j in range(random.randint(0, 10)):
                self.snowflakes.append([i, random.randint(0, 1800)])

    def render(self, screen):
        for i in range(random.randint(0, 10)):
            self.snowflakes.append([random.randint(0, 1800), 0])
        for count, i in enumerate(self.snowflakes):
            pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], 4, 4))
            if random.choice(['RIGHT', 'LEFT']) == 'RIGHT':
                self.snowflakes[count][0] += 4
            else:
                self.snowflakes[count][0] -= 4
            self.snowflakes[count][1] += 2
            if self.snowflakes[count][1] > 893:
                self.snowflakes.pop(count)

        return screen


def fun_exit():
    end_bc = pygame.image.load('data/BG/меню.png')
    exit_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))
    pygame.display.set_caption("Stellar Odyssey")
    # Создаем кнопку "restart_btn"
    quit_btn = Button(110, 70, (66, 170, 255), (0, 191, 255), action=quit)
    # Создаем кнопку "menu_btn"
    menu_btn = Button(130, 70, (66, 170, 255), (0, 191, 255), action=show_menu)
    show = True
    global Attacki
    # Запускаем цикл
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Отображение заднего фона меню
        exit_screen.blit(end_bc, (0, 0))
        # Отображение кнопки "restart_btn"
        quit_btn.draw(510, 350, 'quit', 50)
        # Отображение кнопки "menu_btn"
        menu_btn.draw(210, 350, 'Menu', 50)
        print_text(f'Are you sure you want to quit the game ?', 50, 150, font_size=35)
        # Обновляем экрана
        pygame.display.update()
        clock.tick(60)


def win_game(time):
    """
    Функция для показа выигрыша
    """
    pygame.mixer.music.load('game-win.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    # создание заднего фона
    end_bc = pygame.image.load('data/BG/win.png')
    end_menu_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))
    pygame.display.set_caption("Stellar Odyssey")
    # Создаем кнопку "restart_btn"
    restart_btn = Button(190, 70, (68, 148, 74), (152, 251, 152), action=start_game)
    # Создаем кнопку "menu_btn"
    menu_btn = Button(130, 70, (68, 148, 74), (152, 251, 152), action=show_menu)
    show = True
    global Attacki
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
        print_text(f'{time}', 0, 0, font_size=60)
        print_text(f'Attacks {Attacki}', 0, 0, font_size=60)
        pygame.display.update()
        clock.tick(60)


def end_game(time):
    """
    Функция для показа конца игры
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('zvuki_game_over.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    # создание заднего фона
    end_bc = pygame.image.load('data/BG/gameover.png')
    end_menu_screen = pygame.display.set_mode((START_MENU_WIDTH, START_MENU_HEIGHT))
    pygame.display.set_caption("Stellar Odyssey")
    # Создаем кнопку "restart_btn"
    restart_btn = Button(190, 70, (190, 45, 48), (255, 0, 0), action=start_game)
    # Создаем кнопку "menu_btn"
    menu_btn = Button(130, 70, (190, 45, 48), (255, 0, 0), action=show_menu)
    show = True
    global Attacki
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
        print_text(f'Attacks {Attacki}', 0, 50, font_size=50)
        print_text(f'{time}', 0, 0, font_size=60)
        pygame.display.update()
        clock.tick(60)


def level2():
    pygame.mixer.music.load('fonmusic.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    global game_screen, snow_list, Attacki
    Attacki = 0
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Stellar Odyssey")
    pygame.init()
    background_image = pygame.image.load("data/BG/BG.png").convert()
    running = True
    clock = pygame.time.Clock()
    all_sprites = load_level('FrozenValleys')
    snowsp = []
    mucus = Enemy(980, 500, 1, 16)
    mucus2 = Enemy(1400, 100, -1, 16)
    for i in range(1200):
        x = random.randrange(0, GAME_WIDTH)
        y = random.randrange(0, GAME_HEIGHT)
        snowsp.append([x, y])
    game_status1 = '0'
    snowmans = [Enemy(980, 500, 1, 16), Enemy(1400, 100, -1, 16), Enemy(2500, 235, -1, 16),
                Enemy(3500, 235, -1, 16), Enemy(5504, 500, -1, 16), Enemy(5504, 500, -1, 16), Enemy(384, -35, 1, 16),
                Enemy(7100, 365, -1, 16)]
    game_status = ''
    ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.attack()
        screen.fill(WHITE)
        all_sprites = player.move(all_sprites, snowmans)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        all_sprites = player.collidePlayer(all_sprites)
        screen, snowmans = player.render(screen, snowmans)
        running, game_status = player.game_over(running, 0)
        running, game_status = player.win(running, 0)
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = 'TIME {minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        print_text(f'{out}', 0, 0, font_size=50)
        for i in snowmans:
            i.move()
            screen.blit(i.get_current_image(), (i.x, i.y))
        for i in range(len(snowsp)):
            pygame.draw.circle(screen, WHITE, snowsp[i], 2)
            snowsp[i][1] += 1
            if snowsp[i][1] > GAME_HEIGHT:
                y = random.randrange(-50, -10)
                snowsp[i][1] = y
                x = random.randrange(0, GAME_WIDTH)
                snowsp[i][0] = x
        for snow in snow_list:
            snow.move()
            screen.blit(snow.get_current_image(), (snow.x, snow.y))
            if pygame.sprite.collide_rect(player, snow):
                running, game_status = player.game_over(running, 1)
            if snow.distance >= 550:
                snow_list.remove(snow)
            elif snow.x < 0 or snow.x > GAME_WIDTH:
                snow_list.remove(snow)
        if game_status == 'WIN':
            ticks = 0
            snowmans = [Enemy(980, 500, 1, 16), Enemy(1400, 100, -1, 16), Enemy(2500, 235, -1, 16),
                        Enemy(3500, 235, -1, 16), Enemy(5504, 500, -1, 16), Enemy(5504, 500, -1, 16),
                        Enemy(384, -35, 1, 16), Enemy(7100, 365, -1, 16)]
            win_game(out)
        if player.ydisplacement > 1000:
            running, game_status = player.game_over(running, 1)
        if game_status == 'GAME OVER':
            ticks = 0
            snowmans = [Enemy(980, 500, 1, 16), Enemy(1400, 100, -1, 16), Enemy(2500, 235, -1, 16),
                        Enemy(3500, 235, -1, 16), Enemy(5504, 500, -1, 16), Enemy(5504, 500, -1, 16),
                        Enemy(384, -35, 1, 16), Enemy(7100, 365, -1, 16)]
            end_game(out)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        ticks += 38
    pygame.quit()
    sys.exit()


def show_menu():
    # добавление музыки
    pygame.mixer.music.load('fonmusic.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    # создание заднего фона
    menu_bc = pygame.image.load('data/BG/меню.png')
    # Создаем кнопку "start_btn"
    start_btn = Button(175, 70, (66, 170, 255), (0, 191, 255), action=start_game)
    # Создаем кнопку "quit_btn"
    quit_btn = Button(120, 70, (66, 170, 255), (0, 191, 255), action=fun_exit)
    # Создаем кнопку "quit_btn"
    lev_btn = Button(175, 70, (66, 170, 255), (0, 191, 255), action=level2)
    show = True
    # Запускаем цикл
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Отображение заднего фона меню
        start_menu_screen.blit(menu_bc, (0, 0))
        # Отображение названия игры в главном мееню
        print_text('STELLAR ODYSSEY', 185, 100, font_size=60)
        # Отображение кнопки "start_btn"
        start_btn.draw(330, 200, 'LEVEL 1', 50)
        # Отображение кнопки "quit_btn"
        quit_btn.draw(358, 400, 'quit', 50)
        # Отображение кнопки "lev_btn"
        lev_btn.draw(330, 300, 'LEVEL 2', 50)
        # Обновляем экрана
        pygame.display.update()
        clock.tick(60)


def start_game():
    pygame.mixer.music.load('fonmusic.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    global game_screen, snow_list, Attacki
    Attacki = 0
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Stellar Odyssey")
    pygame.init()
    background_image = pygame.image.load("data/BG/BG.png").convert()
    running = True
    clock = pygame.time.Clock()
    all_sprites = load_level('FrozenValleys')
    snowsp = []
    mucus = Enemy(980, 500, 1, 10)
    mucus2 = Enemy(1400, 100, -1, 10)
    for i in range(1200):
        x = random.randrange(0, GAME_WIDTH)
        y = random.randrange(0, GAME_HEIGHT)
        snowsp.append([x, y])
    snowmans = [Enemy(980, 500, 1, 10), Enemy(1400, 100, -1, 10), Enemy(2500, 235, -1, 10),
                Enemy(3500, 235, -1, 10), Enemy(5504, 500, -1, 10), Enemy(5504, 500, -1, 10)]
    game_status = ''
    ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.attack()
        all_sprites = player.move(all_sprites, snowmans)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        all_sprites = player.collidePlayer(all_sprites)
        screen, snowmans = player.render(screen, snowmans)
        running, game_status = player.game_over(running, 0)
        running, game_status = player.win(running, 0)
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = 'TIME {minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        print_text(f'{out}', 0, 0, font_size=50)
        for i in snowmans:
            i.move()
            screen.blit(i.get_current_image(), (i.x, i.y))
        for i in range(len(snowsp)):
            pygame.draw.circle(screen, WHITE, snowsp[i], 2)
            snowsp[i][1] += 1
            if snowsp[i][1] > GAME_HEIGHT:
                y = random.randrange(-50, -10)
                snowsp[i][1] = y
                x = random.randrange(0, GAME_WIDTH)
                snowsp[i][0] = x
        for snow in snow_list:
            snow.move()
            screen.blit(snow.get_current_image(), (snow.x, snow.y))
            if pygame.sprite.collide_rect(player, snow):
                running, game_status = player.game_over(running, 1)
            if snow.distance >= 350:
                snow_list.remove(snow)
            elif snow.x < 0 or snow.x > GAME_WIDTH:
                snow_list.remove(snow)
        if game_status == 'WIN':
            snowmans = [Enemy(980, 500, 1, 10), Enemy(1400, 100, -1, 10), Enemy(2500, 235, -1, 10),
                        Enemy(3500, 235, -1, 10), Enemy(5504, 500, -1, 10), Enemy(5504, 500, -1, 10)]
            win_game(out)
        if player.ydisplacement > 1000:
            running, game_status = player.game_over(running, 1)
        if game_status == 'GAME OVER':
            ticks = 0
            snowmans = [Enemy(980, 500, 1, 10), Enemy(1400, 100, -1, 10), Enemy(2500, 235, -1, 10),
                        Enemy(3500, 235, -1, 10), Enemy(5504, 500, -1, 10), Enemy(5504, 500, -1, 10)]
            end_game(out)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        ticks += 38
    pygame.quit()
    sys.exit()


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


def print_text(message, x, y, font_color=(255, 255, 255), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    start_menu_screen.blit(text, (x, y))


class Snow(pygame.sprite.Sprite):
    """
    класс снега
    """

    def __init__(self, x, y, napravlenie, speed):
        """
        Инициализия
        """
        self.napravlenie = napravlenie
        self.x = x
        self.y = y
        # скорость движения снега
        self.speed = speed
        self.distance = 0
        self.snow_image = pygame.image.load('data/snowman/снег1.png')
        self.rect = self.snow_image.get_rect()

    def move(self):
        # Изменяем позицию снега
        self.rect = self.snow_image.get_rect(midbottom=(int(self.x + self.snow_image.get_height() / 2),
                                                        int((self.y + self.snow_image.get_height()))))
        if self.napravlenie == 1:
            self.x += self.speed
            self.distance += abs(self.speed)
        else:
            self.x -= self.speed
            self.distance += abs(self.speed)

    def get_current_image(self):
        """
        Возвращение изображение снежинки
        """
        return pygame.transform.scale(self.snow_image, (50, 50))


class Enemy(pygame.sprite.Sprite):
    """
    класс снега
    """

    def __init__(self, x, y, napravlenie, speed):
        """
        Инициализация
        """
        super().__init__()
        self.x = x
        self.y = y
        self.napravlenie = napravlenie
        self.speed = speed
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
        self.attack_duration = 2500
        self.attack_start_time = 0
        self.is_attacking = False
        self.attack_index = 0
        self.animation_speed = 70
        self.rect = self.enemy_image.get_rect()

    def move(self):
        self.rect = self.enemy_image.get_rect(midbottom=(int(self.x + self.enemy_image.get_height() / 2),
                                                         int((self.y + self.enemy_image.get_height()))))
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
                if self.napravlenie == 1:
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
                if self.napravlenie != 1:
                    snow_x = self.x - 80
                else:
                    snow_x = self.x + 200
                snow_y = self.y
                snow = Snow(snow_x, snow_y, self.napravlenie, self.speed)
                snow_list.append(snow)
        else:
            if self.napravlenie != 1:
                self.enemy_image = pygame.image.load('data/snowman/снеговик2.png')
            else:
                self.enemy_image = pygame.image.load('data/snowman/снеговик.png')

    def get_current_image(self):
        """
        Возвращение изображение врага
        """
        return pygame.transform.scale(self.enemy_image, (150, 150))


player = Player()
show_menu()
