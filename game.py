import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import random
from typing import List, Optional, Tuple

# Game settings
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 10

# Shape templates (tetrominoes), each shape is represented by a list of blocks
SHAPES = [
    {"shape": [[1, 1, 1, 1]], "color": (0, 255, 255)},  # I
    {"shape": [[1, 1], [1, 1]], "color": (255, 255, 0)},  # O
    {"shape": [[0, 1, 0], [1, 1, 1]], "color": (128, 0, 128)},  # T
    {"shape": [[1, 0, 0], [1, 1, 1]], "color": (255, 165, 0)},  # L
    {"shape": [[0, 0, 1], [1, 1, 1]], "color": (255, 0, 0)},  # J
    {"shape": [[1, 1, 0], [0, 1, 1]], "color": (0, 255, 0)},  # S
    {"shape": [[0, 1, 1], [1, 1, 0]], "color": (0, 0, 255)}   # Z
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Game variables
score = 0

class Tetris:
    def __init__(self):
        # Board state (holds 0 for empty or 1 for occupied)
        self.board: List[List[int]] = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        # Color board (holds color of pieces, or None if empty)
        self.color_board: List[List[Optional[Tuple[int, int, int]]]] = [[None for _ in range(COLS)] for _ in range(ROWS)]

        self.game_over = False
        self.current_piece: List[List[int]] = [[1, 1, 1, 1]]  # Default piece (I shape)
        self.current_color: Tuple[int, int, int] = (0, 255, 255)  # Default color (cyan for I shape)
        self.x, self.y = COLS // 2 - len(self.current_piece[0]) // 2, 0  # Current piece position

    def new_piece(self):
        piece = random.choice(SHAPES)
        self.current_piece = piece["shape"]
        self.current_color = piece["color"]
        self.x = COLS // 2 - len(self.current_piece[0]) // 2
        self.y = 0

    def rotate_piece(self):
        # Store the current piece configuration before attempting to rotate
        original_piece = self.current_piece
        original_x, original_y = self.x, self.y

        # Rotate the piece by transposing and reversing rows
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

        # Check for collisions with the walls and placed pieces
        if self.check_collision():
            # Revert to the original piece configuration if there is a collision
            self.current_piece = original_piece
            self.x, self.y = original_x, original_y  # Restore original position

    def check_collision(self) -> bool:
        for r, row in enumerate(self.current_piece):
            for c, cell in enumerate(row):
                if cell:
                    if (self.y + r >= ROWS or
                        self.x + c < 0 or
                        self.x + c >= COLS or
                        self.board[self.y + r][self.x + c]):
                        return True
        return False

    def place_piece(self):
        global score
        for r, row in enumerate(self.current_piece):
            for c, cell in enumerate(row):
                if cell:
                    self.board[self.y + r][self.x + c] = 1  # Set the board state to 1 (occupied)
                    self.color_board[self.y + r][self.x + c] = self.current_color  # Set the color of the piece
        self.clear_lines()

    def clear_lines(self):
        global score
        for r in range(ROWS):
            if all(self.board[r]):
                self.board.pop(r)
                self.board.insert(0, [0 for _ in range(COLS)])
                self.color_board.pop(r)
                self.color_board.insert(0, [None for _ in range(COLS)])
                score += 10

    def move_left(self):
        self.x -= 1
        if self.check_collision():
            self.x += 1

    def move_right(self):
        self.x += 1
        if self.check_collision():
            self.x -= 1

    def move_down(self):
        self.y += 1
        if self.check_collision():
            self.y -= 1
            self.place_piece()
            self.new_piece()
            if self.check_collision():
                self.game_over = True

    def draw(self, surface):
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if cell:  # Only draw occupied cells
                    color = self.color_board[r][c]
                    if color:  # Ensure the color is not None
                        pygame.draw.rect(surface, color, (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for r, row in enumerate(self.current_piece):
            for c, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.current_color, ((self.x + c) * BLOCK_SIZE, (self.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Initialize the game object
tetris = Tetris()
tetris.new_piece()

# Game Loop
while not tetris.game_over:
    screen.fill((255, 255, 255))  # Fill the screen with white color

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tetris.game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move_left()
            elif event.key == pygame.K_RIGHT:
                tetris.move_right()
            elif event.key == pygame.K_DOWN:
                tetris.move_down()
            elif event.key == pygame.K_UP:
                tetris.rotate_piece()

    # Move piece down automatically
    tetris.move_down()

    # Draw the game state
    tetris.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set game speed (FPS)
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
