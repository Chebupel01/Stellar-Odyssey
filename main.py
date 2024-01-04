import pygame

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 893
WHITE = (255, 255, 255)
clock = pygame.time.Clock()


class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.start = x
        self.end = SCREEN_WIDTH - 200
        self.last_shoot_time = pygame.time.get_ticks()
        self.left_image_index = 0
        self.right_image_index = 0
        self.left_attack = [pygame.image.load('data/snowman/атака1.png'),
                            pygame.image.load('data/snowman/атака2.png'),
                            pygame.image.load('data/snowman/атака3.png'),
                            pygame.image.load('data/snowman/атака4.png'),
                            pygame.image.load('data/snowman/атака5.png'),
                            pygame.image.load('data/snowman/атака6.png'),
                            pygame.image.load('data/snowman/атака7.png'),
                            pygame.image.load('data/snowman/атака8.png'),
                            pygame.image.load('data/snowman/атака9.png'),
                            pygame.image.load('data/snowman/атака10.png')]
        self.right_attack = [pygame.image.load('data/snowman/атакаслева1.png'),
                             pygame.image.load('data/snowman/атакасл2.png'),
                             pygame.image.load('data/snowman/атакасл3.png'),
                             pygame.image.load('data/snowman/атакасл4.png'),
                             pygame.image.load('data/snowman/атакасл5.png'),
                             pygame.image.load('data/snowman/атакасл6.png'),
                             pygame.image.load('data/snowman/атакасл7.png'),
                             pygame.image.load('data/snowman/атакасл8.png'),
                             pygame.image.load('data/snowman/атакасл9.png'),
                             pygame.image.load('data/snowman/атакасл10.png')]
        self.enemy_images = self.left_attack

    def move(self):
        current_time = pygame.time.get_ticks()
        time_since_last_shoot = current_time - self.last_shoot_time
        if time_since_last_shoot >= 5000:
            self.shoot()
            self.last_shoot_time = current_time
        if self.speed < 0:
            if self.x > self.start - self.speed:
                self.x += self.speed
            else:
                self.speed *= -1
                self.x += self.speed
            self.enemy_images = self.left_attack
        else:
            if self.x < self.end + self.speed:
                self.x += self.speed
            else:
                self.speed *= -1
                self.x += self.speed
            self.enemy_images = self.right_attack

    def shoot(self):
        if self.speed < 0:
            self.left_image_index = (self.left_image_index + 1) % len(self.left_attack)
            self.enemy_images = self.left_attack
        else:
            self.right_image_index = (self.right_image_index + 1) % len(self.right_attack)
            self.enemy_images = self.right_attack

    def get_current_image(self):
        return pygame.transform.scale(
            self.enemy_images[self.left_image_index if self.speed < 0 else self.right_image_index], (200, 200))


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
    pygame.display.update()
    clock.tick(30)
pygame.quit()
