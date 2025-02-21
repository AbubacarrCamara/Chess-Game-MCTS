import pygame

from Chess_MCTS import Game

# Starts pygame
pygame.init()

# Sets window dimensions 
window_size = 640
square_size = window_size // 8
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption('Chess Game')
clock = pygame.time.Clock()

# Draws the board onto the screen
def draw_board(surface):
    light_color = (240, 217, 181)
    dark_color = (181, 136, 99)
    for row in range(8):
        for col in range(8):
            # Chooses color based on the sum of row and col
            if (row + col) % 2 == 0:
                color = light_color
            else:
                color = dark_color
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(surface, color, rect)

# Loads pieces into the game
piece_images = {
    'white_king' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wK.svg'),
    'white_queen' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wQ.svg'),
    'white_knight' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wN.svg'),
    'white_bishop' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wB.svg'),
    'white_rook' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wR.svg'),
    'white_pawn' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/wP.svg'),
    'black_king' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bK.svg'),
    'black_queen' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bQ.svg'),
    'black_knight' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bN.svg'),
    'black_bishop' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bB.svg'),
    'black_rook' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bR.svg'),
    'black_pawn' : pygame.image.load('C:/Users/Stabu/OneDrive - University of Keele/Chess Game/Piece Images/monarchy/bP.svg'),

    
}

def draw_pieces(surface, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                key = f'{piece.color}_{piece.piece_type.lower()}'
                img = piece_images.get(key)
                if img: 
                    # Scales images to fit squares 
                    img = pygame.transform.scale(img, (square_size - 10, square_size - 10))

                    surface.blit(img, (col * square_size , row * square_size))


def get_board_position(mouse_pos):
    x, y = mouse_pos 
    col = x // square_size
    row = y // square_size
    return (row, col)

game = Game()

selected_square = None
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # When game is over, app waits for mouse or button press to reset 
        if game_over:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            board_pos = get_board_position(pygame.mouse.get_pos())
            if selected_square is None:
                selected_square = board_pos
            else:
                start, end = selected_square, board_pos
                if game.board.move_piece(start, end):
                    print('Move executed')

                    if game.board.is_checkmate(game.board.board, game.board.current_turn):
                        print('Checkmate')
                        game_over = True
                    
                else:
                    print('Invalid move')
                selected_square = None

    draw_board(window)
    draw_pieces(window, game.board.board)

    # If game over displays a game over message
    if game_over:
        font = pygame.font.SysFont('Arial', 32)
        text_surface = font.render('Checkmate! Press any key to exit.', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(window_size//2, window_size//2))
        window.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
