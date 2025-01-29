import pygame
import sys

# Constants for the players
BLACK = 'B'
WHITE = 'W'
EMPTY = '.'

# Colors
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 128, 0)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Grid size
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

# Directions to check for valid moves (horizontal, vertical, diagonal)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1),
              (-1, -1), (-1, 1), (1, -1), (1, 1)]


def initialize_board():
    board = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
    board[3][3] = board[4][4] = WHITE
    board[3][4] = board[4][3] = BLACK
    return board


def draw_text(text, size, x, y, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    SCREEN.blit(text_surface, text_rect)


def initialize_game():
    board = initialize_board()
    current_player = BLACK
    game_over = False
    winner = None
    quit_game = False
    return board, current_player, game_over, winner, quit_game


def show_start_screen(winner=None):
    waiting = True
    redraw = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        if redraw:
            redraw = False
            SCREEN.fill(BACKGROUND_COLOR)

            if winner != None:
                draw_text("Game Over", 50, WIDTH //
                          2, HEIGHT // 4, center=True)
                draw_text(f"{winner} wins!", 30, WIDTH //
                          2, HEIGHT // 2, center=True)
                pygame.draw.rect(SCREEN, (100, 100, 255),
                                 (WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 50))
                draw_text("Restart Game", 30, WIDTH // 2,
                          HEIGHT // 1.5 + 25, center=True)
            else:
                draw_text("Reversi (Othello)", 50, WIDTH //
                          2, HEIGHT // 4, center=True)
                pygame.draw.rect(SCREEN, (100, 100, 255),
                                 (WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 50))
                draw_text("Start Game", 30, WIDTH // 2,
                          HEIGHT // 1.5 + 25, center=True)

            pygame.display.update()
            redraw = False


def draw_board(board):
    SCREEN.fill(BACKGROUND_COLOR)

    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(SCREEN, GRID_COLOR, (col * SQUARE_SIZE,
                             row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

    # Draw the pieces
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == BLACK:
                pygame.draw.circle(SCREEN, BLACK_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE //
                                   2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 4)
            elif board[row][col] == WHITE:
                pygame.draw.circle(SCREEN, WHITE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE //
                                   2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 4)

    pygame.display.flip()


def draw_player_turn_indicator(player):
    pygame.display.set_caption(f"{player}'s Turn")


def is_valid_move(board, row, col, player):
    if board[row][col] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        has_opponent_between = False

        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if board[r][c] == opponent:
                has_opponent_between = True
            elif board[r][c] == player and has_opponent_between:
                return True
            elif board[r][c] == EMPTY:
                break
            r += dr
            c += dc

    return False


def place_move(board, row, col, player):
    board[row][col] = player

    opponent = WHITE if player == BLACK else BLACK

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        pieces_to_flip = []

        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if board[r][c] == opponent:
                pieces_to_flip.append((r, c))
            elif board[r][c] == player:
                for pr, pc in pieces_to_flip:
                    board[pr][pc] = player
                break
            elif board[r][c] == EMPTY:
                break
            r += dr
            c += dc


def has_valid_moves(board, player):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if is_valid_move(board, r, c, player):
                return True
    return False


def play_game():
    board, current_player, game_over, winner, quit_game = initialize_game()

    while True:
        draw_board(board)
        draw_player_turn_indicator(current_player)
        # Check if the current player has any valid moves
        if not has_valid_moves(board, current_player):
            current_player = WHITE if current_player == BLACK else BLACK
            if not has_valid_moves(board, current_player):
                # No valid moves for either player, game over
                winner = BLACK if sum(row.count(BLACK) for row in board) > sum(
                    row.count(WHITE) for row in board) else WHITE
                game_over = True

        # Handle events (clicking on the board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if is_valid_move(board, row, col, current_player):
                    place_move(board, row, col, current_player)
                    current_player = WHITE if current_player == BLACK else BLACK

            # Restart the game when the button is clicked
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 4 <= x <= WIDTH // 4 + WIDTH // 2 and HEIGHT // 1.5 <= y <= HEIGHT // 1.5 + 50:
                    board, current_player, game_over, winner, quit_game = initialize_game()

        # Display the winner message
        if game_over:
            break

        pygame.display.update()

        if quit_game:
            pygame.quit()
            sys.exit()
    return winner


if __name__ == "__main__":
    winner = None
    while (show_start_screen(winner)):
        winner = play_game()
