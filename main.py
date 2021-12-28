import pygame
import random

pygame.font.init()

WIDTH = 800
HEIGHT = 700
grid_width = 300
grid_height = 600
block_size = 30

top_left_x = (WIDTH - grid_width) // 2
top_left_y = HEIGHT - grid_height

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
    ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
      ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Shape(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid():
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
    return grid


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx + grid_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy + i*block_size), (sx + j*block_size, sy + grid_height))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (128, 128, 128), (top_left_x, top_left_y, grid_width, grid_height), 1)

    draw_grid(surface, grid)


def main(screen):
    running = True
    shape1 = Shape(5, 0, random.choice(shapes))
    clock = pygame.time.Clock()

    while running:
        grid = create_grid()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape1.x -= 1
                    if not(valid_space(shape1, grid)):
                        shape1.x += 1

                elif event.key == pygame.K_RIGHT:
                    shape1.x += 1
                    if not(valid_space(shape1, grid)):
                        shape1.x -= 1

                elif event.key == pygame.K_DOWN:
                    shape1.y += 1
                    if not(valid_space(shape1, grid)):
                        shape1.y -= 1

                elif event.key == pygame.K_UP:
                    shape1.rotation += 1
                    if not(valid_space(shape1, grid)):
                        shape1.rotation -= 1

        draw_window(screen, grid)
        pygame.display.update()


def main_menu(screen):
    run = True
    while run:
        screen.fill((0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(screen)

    pygame.display.quit()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

main_menu(screen)