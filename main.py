import pygame
import random
import sys
import os
import sqlite3


class Shape:
    shapes = [
        [
            [4, 5, 6, 7],
            [2, 6, 10, 14],
            [8, 9, 10, 11],
            [1, 5, 9, 13]
        ],
        [
            [2, 4, 5, 6],
            [1, 5, 9, 10],
            [4, 5, 6, 8],
            [0, 1, 5, 9]
        ],
        [
            [0, 4, 5, 6],
            [1, 2, 5, 9],
            [4, 5, 6, 10],
            [1, 5, 8, 9]
        ],
        [
            [0, 1, 5, 6],
            [2, 5, 6, 9],
            [4, 5, 9, 10],
            [1, 4, 5, 8]
        ],
        [
            [1, 2, 4, 5],
            [1, 5, 6, 10],
            [5, 6, 8, 9],
            [0, 4, 5, 9]
        ],
        [
            [1, 4, 5, 6],
            [1, 5, 6, 9],
            [4, 5, 6, 9],
            [1, 4, 5, 9]
        ],
        [
            [1, 2, 5, 6],
            [1, 2, 5, 6],
            [1, 2, 5, 6],
            [1, 2, 5, 6]
        ]
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.type = random.randint(0, 6)
        self.colour = self.type + 1

        self.rotations = 0

    def rotate(self):
        self.rotations = (self.rotations + 1) % 4

    def image(self):
        return self.shapes[self.type][self.rotations]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))

        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


class Tetris:
    def __init__(self, height, width):
        self.field = []
        self.score = 0

        self.height = height
        self.width = width
        self.last_line = 1

        self.figure = None
        self.anim_k = 0
        self.anim = False
        self.state = "??????????"
        for i in range(self.height):
            new_line = []

            for j in range(self.width):
                new_line.append(0)

            self.field.append(new_line)

    def new_shape(self):
        self.figure = Shape(3, 0)

    def cross(self):
        crossing = False

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        crossing = True

        return crossing

    def clear_lines(self):
        row = -1
        lines = 0

        for i in self.field:
            k = self.width
            row += 1

            for j in i:
                if j != 0:
                    k -= 1

            if k == 0:
                del self.field[row]
                self.last_line = row

                new_line = []
                self.anim = True
                for j in range(self.width):
                    new_line.append(0)

                self.field.insert(0, new_line)
                lines += 1

        self.anim_k = lines
        self.score += lines ** 2

        self.figure = None

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.colour

        self.clear_lines()
        self.new_shape()

        if self.cross() == True:
            self.state = "????????????????"

    def hard_drop(self):
        while not self.cross() == True:
            self.figure.y += 1

        if self.cross() == True:
            self.figure.y -= 1
            self.freeze()

    def soft_drop(self):
        self.figure.y += 1

        if self.cross() == True:
            self.figure.y -= 1
            self.freeze()

    def move_side(self, direction):
        o = self.figure.x
        self.figure.x += direction

        if self.cross() == True:
            self.figure.x = o

    def press_up(self):
        o = self.figure.rotations
        self.figure.rotate()

        if self.cross() == True:
            self.figure.rotations = o

    def animat(self):
        self.anim = False


def terminate():
    pygame.quit()
    sys.exit()


def final_menu(screen, result):
    con = sqlite3.connect("tetris.db")
    cur = con.cursor()

    results = cur.execute("""SELECT * FROM record""").fetchall()

    a = []
    for i, elem in enumerate(results):
        for j, val in enumerate(elem):
            a.append(str(val))

    record = 0

    for i in a:
        if int(i) > record:
            record = int(i)

    run = True
    while run:
        screen.fill((0, 0, 0))

        fon = pygame.transform.scale(load_image('final.jpg'), (700, 900))
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont('Calibri', 60, True, False)

        string_rendered = font.render('???? ??????????????????!', 2, pygame.Color('white'))
        screen.blit(string_rendered, [140, 100])

        string_rendered = font.render('?????? ??????????????????: ' + str(result), 2, pygame.Color('white'))
        screen.blit(string_rendered, [130, 300])

        string_rendered = font.render('?????? ????????????: ' + str(record), 2, pygame.Color('white'))
        screen.blit(string_rendered, [150, 500])

        font1 = pygame.font.SysFont('Calibri', 25, True, False)

        string_rendered = font1.render('?????????????? Enter ?????? Backspace, ?????????? ??????????', 1,
                                       (0, 0, 0))
        screen.blit(string_rendered, [10, 860])

        string_rendered = font1.render('?????????????? SPACE, ?????????? ???????????? ????????????', 1,
                                       (0, 0, 0))
        screen.blit(string_rendered, [10, 820])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    start_menu(screen)

                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                    exit(0)

        pygame.display.flip()

    pygame.display.quit()


def main_menu(screen, speed):
    pygame.init()
    pause = False

    image = load_image('bl.jfif')
    image = pygame.transform.scale(image, (40, 40))

    all_sprites = pygame.sprite.Group()

    colours = [
        (0, 255, 255),
        (255, 165, 0),
        (0, 0, 255),
        (255, 0, 0),
        (0, 255, 0),
        (255, 0, 255),
        (255, 255, 0), ]

    anim_k = 0

    game = Tetris(20, 10)
    clock = pygame.time.Clock()

    hold_down = False
    refresh = 0

    while True:
        if game.figure is None:
            game.new_shape()

        if not pause:
            refresh += speed
            if game.anim:
                anim_k += 1
                if anim_k % 15 == 0:
                    game.animat()
                    all_sprites = pygame.sprite.Group()

            if refresh % (20 - game.score // 20) == 0:
                if game.state == "??????????":
                    game.soft_drop()

        if hold_down == True:
            if game.state == "??????????":
                game.soft_drop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key != pygame.KMOD_ALT:
                pause = False

            if not pause:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_UP:
                        game.press_up()

                    if event.key == pygame.K_DOWN:
                        hold_down = True

                    if event.key == pygame.K_LEFT:
                        game.move_side(-1)

                    if event.key == pygame.K_RIGHT:
                        game.move_side(1)

                    if event.key == pygame.K_SPACE:
                        game.hard_drop()

                    if event.key == pygame.K_ESCAPE:
                        game.__init__(20, 10)

                    if event.key == pygame.K_p:
                        pause = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    hold_down = False

        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('fon.jpg'), (700, 900))
        screen.blit(fon, (0, 0))

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, (100, 100, 100), [100 + 40 * j, 60 + 40 * i, 40, 40], 1)

                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colours[game.field[i][j] - 1],
                                     [100 + 40 * j + 1, 60 + i * 40 + 1, 36, 36])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in game.figure.image():
                        pygame.draw.rect(screen, colours[game.figure.colour - 1],
                                         [100 + 40 * (j + game.figure.x) + 1,
                                          60 + 40 * (i + game.figure.y) + 1,
                                          36, 36])

        if pause:
            font = pygame.font.SysFont('Calibri', 60, True, False)

            string_rendered = font.render('???????? ????????????????????????????!', 1, (255, 100, 100))
            screen.blit(string_rendered, [70, 410])

        if game.state == "????????????????":
            print(game.score * 10)
            con = sqlite3.connect("tetris.db")
            cur = con.cursor()

            qwer = f""" INSERT INTO record(result) VALUES({str(game.score * 10)})"""

            cur.executescript(qwer)
            final_menu(screen, game.score * 10)

        font = pygame.font.SysFont('Calibri', 60, True, False)

        string_rendered = font.render('????????:', 2, pygame.Color('white'))
        screen.blit(string_rendered, [520, 60])

        string_rendered = font.render(str(game.score * 10), 2, pygame.Color('white'))
        screen.blit(string_rendered, [530, 130])

        string_rendered = font.render('T', 2, pygame.Color('white'))
        screen.blit(string_rendered, [570, 250])

        string_rendered = font.render('E', 2, pygame.Color('white'))
        screen.blit(string_rendered, [570, 320])

        string_rendered = font.render('T', 2, pygame.Color('white'))
        screen.blit(string_rendered, [570, 390])

        string_rendered = font.render('R', 2, pygame.Color('white'))
        screen.blit(string_rendered, [570, 460])

        string_rendered = font.render('I', 2, pygame.Color('white'))
        screen.blit(string_rendered, [577, 530])

        string_rendered = font.render('S', 2, pygame.Color('white'))
        screen.blit(string_rendered, [570, 600])

        font1 = pygame.font.SysFont('Calibri', 30, True, False)

        string_rendered = font1.render('??????????: P', 1, (255, 100, 100))
        screen.blit(string_rendered, [540, 850])

        string_rendered = font1.render('????????????: Esc', 1, (255, 100, 100))
        screen.blit(string_rendered, [540, 800])

        font2 = pygame.font.SysFont('Calibri', 20, True, False)

        string_rendered = font2.render('??????????: Backspace', 1, (255, 100, 100))
        screen.blit(string_rendered, [540, 760])

        if game.anim:
            for j in range(0, game.anim_k):
                for i in range(10):
                    sprite1 = pygame.sprite.Sprite()
                    sprite1.image = image

                    sprite1.rect = sprite1.image.get_rect()

                    sprite1.rect.x = 100 + 40 * i
                    sprite1.rect.y = 20 - 40 * j + (game.last_line + 1) * 40

                    all_sprites.add(sprite1)

            all_sprites.draw(screen)

        clock.tick(60)
        pygame.display.flip()


def start_menu(screen):
    run = True
    clock = pygame.time.Clock()

    FPS = 60
    fon = pygame.transform.scale(load_image('zastavka.jpg'), (700, 900))

    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))

    while run:
        fon = pygame.transform.scale(load_image('zastavka.jpg'), (700, 900))

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont('Calibri', 100, True, False)

        string_rendered = font.render('T E T R I S', 2, (255, 50, 50))
        screen.blit(string_rendered, [160, 100])

        font = pygame.font.SysFont('Calibri', 50, True, False)

        string_rendered = font.render('?????????? ????????????????????!', 2, pygame.Color('white'))
        screen.blit(string_rendered, [150, 400])

        string_rendered = font.render('???????????????? ??????????????????:', 2, pygame.Color('white'))
        screen.blit(string_rendered, [130, 500])

        font1 = pygame.font.SysFont('Calibri', 40, True, False)

        string_rendered = font1.render('?????????? ???? ???????????? 1, 2, 3, 4 ?????? 5.', 2, pygame.Color('white'))
        screen.blit(string_rendered, [80, 600])

        font2 = pygame.font.SysFont('Calibri', 20, True, False)

        string_rendered = font2.render('??????????: Backspace', 1, (255, 255, 100))
        screen.blit(string_rendered, [540, 850])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.key == pygame.K_1:
                    main_menu(screen, 1)

                if event.key == pygame.K_2:
                    main_menu(screen, 2)

                if event.key == pygame.K_3:
                    main_menu(screen, 3)

                if event.key == pygame.K_4:
                    main_menu(screen, 4)

                if event.key == pygame.K_5:
                    main_menu(screen, 5)

                if event.key == pygame.K_BACKSPACE:
                    exit(0)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.quit()


pygame.init()
screen = pygame.display.set_mode(size=(700, 900))
pygame.display.set_caption("Tetris")
start_menu(screen)