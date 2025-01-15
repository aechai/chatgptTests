import os
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, ORANGE, BLUE]

# Create game grid
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            if grid[y][x] != BLACK:
                pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color, ((self.x + j) * BLOCK_SIZE, (self.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + j
                new_y = tetromino.y + i
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return True
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return True
    return False

def merge_tetromino(tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[tetromino.y + i][tetromino.x + j] = tetromino.color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    cleared_lines = GRID_HEIGHT - len(new_grid)
    new_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(cleared_lines)] + new_grid
    grid = new_grid
    return cleared_lines

# Initialize game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
current_tetromino = Tetromino()
running = True
score = 0

while running:
    screen.fill(BLACK)
    draw_grid(screen)
    current_tetromino.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.move(-1, 0)
                if check_collision(current_tetromino):
                    current_tetromino.move(1, 0)
            if event.key == pygame.K_RIGHT:
                current_tetromino.move(1, 0)
                if check_collision(current_tetromino):
                    current_tetromino.move(-1, 0)
            if event.key == pygame.K_DOWN:
                current_tetromino.move(0, 1)
                if check_collision(current_tetromino):
                    current_tetromino.move(0, -1)
            if event.key == pygame.K_UP:
                current_tetromino.rotate()
                if check_collision(current_tetromino):
                    for _ in range(3):
                        current_tetromino.rotate()

    current_tetromino.move(0, 1)
    if check_collision(current_tetromino):
        current_tetromino.move(0, -1)
        merge_tetromino(current_tetromino)
        clear_lines()
        current_tetromino = Tetromino()
        if check_collision(current_tetromino):
            running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
