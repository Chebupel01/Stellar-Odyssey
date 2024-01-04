import pygame

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)
clock = pygame.time.Clock()


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
        self.snowball_image = pygame.image.load('data/snowman/снег1.png')
        self.snowball_x = 0
        self.snowball_y = 0
        self.snowball_speed = 8
        self.show_snowball = False
        self.snowball_direction = 1
        self.throw_animation_done = False

    def move(self):
        current_time = pygame.time.get_ticks()
        time_since_last_shoot = current_time - self.last_shoot_time
        if time_since_last_shoot >= self.attack_duration and not self.is_attacking:
            self.is_attacking = True
            self.attack_start_time = current_time
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

                if not self.throw_animation_done and time_since_last_shoot >= self.attack_duration + (
                        len(self.left_attack) * self.animation_speed):
                    self.show_snowball = True
                    self.snowball_x = self.x
                    self.snowball_y = self.y
                    self.snowball_direction = 1 if self.speed > 0 else -1
                    self.throw_animation_done = True

            if time_since_last_shoot >= self.attack_duration + (
                    len(self.left_attack) * self.animation_speed) + 2000:
                self.is_attacking = False
                self.attack_index = 0
                self.last_shoot_time = current_time
                self.throw_animation_done = False

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
background_image = pygame.image.load("data/BG/BG.png").convert()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    mucus.move()
    screen.blit(mucus.get_current_image(), (mucus.x, mucus.y))
    if mucus.show_snowball:
        mucus.snowball_x += mucus.snowball_speed * mucus.snowball_direction
        screen.blit(mucus.snowball_image, (mucus.snowball_x, mucus.snowball_y))
    pygame.display.update()
    clock.tick(30)
pygame.quit()
