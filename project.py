import sys
import random
import pygame
import os
import time

WIDTH = 600
HEIGHT = 800
FPS = 60
STEP = 100

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

pygame.mixer.init()
PLAY = pygame.mixer.Sound("data/play.mp3")
PLAY.play(-1, 0)
PLAY.set_volume(0.2)

BOOM = pygame.mixer.Sound('data/boom.mp3')
BOOM.set_volume(0.3)

BULLETSHOT = pygame.mixer.Sound('data/bullet.mp3')
BULLETSHOT.set_volume(0.3)

GAME_OVER_MUSIC = pygame.mixer.Sound('data/game_over.mp3')
GAME_OVER_MUSIC.set_volume(0.3)

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 70)

bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
explosions = pygame.sprite.Group()
heroes = pygame.sprite.Group()

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
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["",
                  "",
                  "",
                  "",
                  "",
                  "ИГРА ЗВЁЗДНЫЕ ВОЙНЫ.", "",
                  "Правила игры:",
                  "надо стрелять по надвигающимся",
                  "на тебя кораблям.",
                  "",
                  "Управление клавишами вправо влево,",
                  "чтобы стрелять нажмите на левую кнопку мыши."]

    fon = pygame.transform.scale(load_image('fon1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 34)
    text_coord = 70
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
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


GAME_OVER = load_image('fon2.jpg')
start_screen()


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, step, image, group):
        super().__init__(group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT

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
        BULLETSHOT.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


ship_image = load_image('ship.png')
zlodei_image = load_image('zlodei.png')
fon = pygame.transform.scale(load_image('fon1.png'), (WIDTH, HEIGHT))

ship = Ship(244, 688, 50, 'ship.png', heroes)

screen.blit(fon, (0, 0))
all_sprites.add(ship)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = zlodei_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 4)


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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = boombs[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(boombs):
                self.kill()
            else:
                center = self.rect.center
                self.image = boombs[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def game_over():
    GAME_OVER_MUSIC.play()
    fon = pygame.transform.scale(GAME_OVER, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text(screen, 'Счет: ' + str(score), 50, WIDTH / 2, HEIGHT / 5)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


for i in range(10):
    newmob()

boombs = [load_image('regularExplosion01.png'),
          load_image('regularExplosion02.png'),
          load_image('regularExplosion03.png'),
          load_image('regularExplosion04.png'),
          load_image('regularExplosion05.png'),
          load_image('regularExplosion06.png'),
          load_image('regularExplosion07.png'),
          load_image('regularExplosion08.png')
          ]

score = 0
running = True
k = 0
while running:

    k += 1
    all_sprites.update()

    # проверка, не попала ли пуля в моб
    shots_fired = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for shots in shots_fired:
        BOOM.play()
        score += 50
        expl = Explosion(shots.rect.center)
        all_sprites.add(expl)
        newmob()

    #  Проверка, не ударил ли моб игрока
    hits = pygame.sprite.groupcollide(heroes, mobs, True, True)
    for sl in hits:
        expl = Explosion(sl.rect.center)
        all_sprites.add(expl)
        newmob()
        running = False

    screen.blit(fon, (0, 0))
    heroes.draw(screen)
    text(screen, str(score), 50, WIDTH / 2, 10)
    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ship.shoot()

    clock.tick(FPS)
    pygame.display.flip()

screen2 = pygame.display.set_mode(size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_over()
    pygame.display.flip()

    clock.tick(FPS)

terminate()
