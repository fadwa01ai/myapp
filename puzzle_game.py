import sys
import random
import pygame

# إعدادات الشاشة والألوان
BOARD_SIZE = 4  # شبكة 4x4
TILE_SIZE = 100
MARGIN = 5
WINDOW_SIZE = BOARD_SIZE * TILE_SIZE + (BOARD_SIZE + 1) * MARGIN

BG_COLOR = (24, 28, 36)
TILE_COLOR = (0, 210, 255)
TEXT_COLOR = (10, 14, 23)
EMPTY_COLOR = (40, 48, 62)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Slide Puzzle Game 🧩")
font = pygame.font.Font(None, 50)


def create_board():
    tiles = list(range(1, BOARD_SIZE * BOARD_SIZE)) + [None]
    random.shuffle(tiles)
    return [
        tiles[i : i + BOARD_SIZE] for i in range(0, len(tiles), BOARD_SIZE)
    ]


def find_empty(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] is None:
                return r, c


def move_tile(board, row, col):
    empty_r, empty_c = find_empty(board)
    if (abs(empty_r - row) == 1 and empty_c == col) or (
        abs(empty_c - col) == 1 and empty_r == row
    ):
        board[empty_r][empty_c], board[row][col] = (
            board[row][col],
            board[empty_r][empty_c],
        )


def draw_board(board):
    screen.fill(BG_COLOR)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            val = board[r][c]
            x = c * TILE_SIZE + (c + 1) * MARGIN
            y = r * TILE_SIZE + (r + 1) * MARGIN

            if val is not None:
                pygame.draw.rect(
                    screen,
                    TILE_COLOR,
                    (x, y, TILE_SIZE, TILE_SIZE),
                    border_radius=8,
                )
                text = font.render(str(val), True, TEXT_COLOR)
                text_rect = text.get_rect(
                    center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                )
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(
                    screen,
                    EMPTY_COLOR,
                    (x, y, TILE_SIZE, TILE_SIZE),
                    border_radius=8,
                )
    pygame.display.flip()


def main():
    board = create_board()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col = mx // (TILE_SIZE + MARGIN)
                row = my // (TILE_SIZE + MARGIN)
                if row < BOARD_SIZE and col < BOARD_SIZE:
                    move_tile(board, row, col)

        draw_board(board)
        clock.tick(30)


if __name__ == "__main__":
    main()