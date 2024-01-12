import sys
import random
import pygame
import os

WIDTH = 600
HEIGHT = 600
FPS = 60
STEP = 100

YELLOW = (255, 255, 0)

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 70)

bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Звёздные войны")


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["ИГРА ЗВЁЗДНЫЕ ВОЙНЫ", "",
                  "Правила игры:",
                  "надо стрелять по надвигающимся на тебя кораблям"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, step, image, group):
        super().__init__(group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.speed = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speed = -10
        if key[pygame.K_RIGHT]:
            self.speed = 10
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


heroes = pygame.sprite.Group()
ship = Ship(244, 488, 50, 'ship3.png', heroes)

fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
screen.blit(fon, (0, 0))

all_sprites.add(ship)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('zlodei.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

running = True
k = 0
while running:
    k += 1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    shells = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for missile in shells:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)

    if k == 15:
        ship.shoot()
        k = 0

    all_sprites.update()

    screen.blit(fon, (0, 0))
    heroes.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

terminate()
