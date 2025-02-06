class Game:
    def __init__(self):
        self.board = Board()

    def start(self):
        while True:
            self.board.display_board()
            print("Current turn:", self.board.current_turn)
            move_input = input("Enter your move (e.g., 'e2 e4'): ")
            try:
                start, end = self.parse_move(move_input)
            except Exception as e:
                print("Invalid input format. Please try again.")
                continue

            if self.board.move_piece(start, end):
                print("Move executed")
            else:
                print("Invalid move, try again.")

            if self.board.is_checkmate(self.board, self.board.current_turn):
                print(f"Checkmate! {self.board.opponent_color(self.board.current_turn).capitalize()} wins!")
                break  # Ends the game
                
    def parse_move(self, move_input):
        '''
        Converts moves from algebraic expression into board indices.
        '''
        start_str, end_str = move_input.split()
        start = self.algebraic_to_index(start_str)
        end = self.algebraic_to_index(end_str)
        return start, end 

    def algebraic_to_index(self, pos_str):
        """
        Convert a position string like 'e2' to a tuple of board indices.
        Assume the bottom left is 'a1' and the board is 0-indexed.
        """
        files = 'abcdefgh'
        ranks = '12345678'
        col = files.index(pos_str[0])
        row = 8 - int(pos_str[1])
        return (row, col)

class Board:
    def __init__(self):
        # Initialize an 8x8 board as an instance variable
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.current_turn = 'white'
        self.en_passant_target = None
        self.king_positions = {'white': None, 'black': None}

    def __getitem__(self, index):
        return self.board[index]

    def setup_board(self):

        # Places the Kings
        self.board[0][4] = King('black', first_move=True)
        self.board[7][4] = King('white', first_move=True)

        # Places the Queens
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        # Places the Bishops
        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')

        self.board[7][2] = Bishop('white')
        self.board[7][5] = Bishop('white')

        # Places the Knights
        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        
        self.board[7][1] = Knight('white')
        self.board[7][6] = Knight('white')

        # Places the Rooks
        self.board[0][0] = Rook('black', first_move=True)
        self.board[0][7] = Rook('black', first_move=True)

        self.board[7][0] = Rook('white', first_move=True)
        self.board[7][7] = Rook('white', first_move=True)



        # Place black pawns on row 1 (index 1)
        for col in range(8):
            self.board[1][col] = Pawn('black', direction=1, first_move=True)
        # Place white pawns on row 6 (index 6)
        for col in range(8):
            self.board[6][col] = Pawn('white', direction=-1, first_move=True)

    def display_board(self):
        # Maps piece type to a symbol
        piece_symbols = {
            'King' : 'K',
            'Queen' : 'Q',
            'Bishop' : 'B',
            'Knight' : 'N',
            'Rook' : 'R',
            'Pawn' : 'P',
        }

        for row in self.board:
            row_str = ' '.join(['.' if cell is None else piece_symbols.get(cell.piece_type, '?') for cell in row
            ])
            print(row_str)

    def get_piece(self, position):
        '''
        Returns the piece at the given board position.
        return a tuple (row, col)
        '''
        row, col = position
        return self.board[row][col]

    def move_piece(self, start, end):
        """
        Execute a move from the start position to the end position.
        This method:
          - Validates the move.
          - Updates the board.
          - Switches the current turn.
        Returns True if the move was executed successfully, or False otherwise.
        """
        # Retrieves the piece at the starting position 
        piece = self.get_piece(start)
        if piece is None:
            print("There is no piece at the start position!")
            return False

        # Checks if piece belongs to the current player
        if piece.color != self.current_turn:
            print('It is not your turn!')
            return False

        if piece.piece_type == 'King':
            legal_moves = piece.possible_moves(self.board, start, castle=True)
        elif piece.piece_type == 'Pawn':
            legal_moves = piece.possible_moves(self.board, start, en_passant=self.en_passant_target)
        else:
            legal_moves = piece.possible_moves(self.board, start)

        if end not in legal_moves:
            print("That move is not legal!")
            return False
        
        # Detects if this is a castaling move
        if piece.piece_type == 'King' and abs(end[1] - start[1]) == 2:
            row = start[0]
            # Kingside castling
            if end[1] > start[1]:
                # The rook on the kingside should move one space to the right of where the king starts 
                rook = self.board[row][7]
                self.board[row][start[1] + 1] = rook
                self.board[row][7] = None

            else:
                rook = self.board[row][0]
                self.board[row][start[1] - 1] = rook
                self.board[row][0] = None

            if hasattr(rook, 'first_move'):
                rook.first_move = False

        # Checks for en passant capture for pawns
        if piece.piece_type == 'Pawn':
            if abs(end[1] - start[1]) == 1 and self.board[end[0]][end[1]] is None:
                captured_row = start[0]
                captured_col = end[1]
                print("En passant capture!")
                self.board[captured_row][captured_col] = None
        # Executes the move
        self.board[end[0]][end[1]] = piece

        # Emptys the starting cell
        self.board[start[0]][start[1]] = None
        piece.history.append((start, end))
        if hasattr(piece, 'first_move'):
            piece.first_move = False

        if piece.piece_type == 'Pawn' and abs(end[0] - start[0]) == 2:
            self.en_passant_target = ((start[0] + end[0] // 2), start[1])
        else:
            self.en_passant_target = None

        # The below creates a copy of the board to ensure the the next move does not lead to the king being in check 
        temp_board = self.copy_board_from(self.board)
        temp_board[end[0]][end[1]] = piece
        temp_board[start[0]][start[1]] = None


        king_pos = self.find_king(temp_board, self.current_turn)

        opponent = 'black' if self.current_turn == 'white' else 'white'
        if self.is_square_attacked(temp_board, king_pos, opponent):
            print('Move not allowed: King would be in check!')
            return False
        else:

            # Below executes the move
            # Places piece on at the destination 
            self.board[end[0]][end[1]] = piece

            # Empty's the starting cell
            self.board[start[0]][start[1]] = None

            # Updates the piece's history (or other flags such as first move)
            piece.history.append((start, end))
            if hasattr(piece, 'first_move'):
                piece.first_move = False

            # Checks for checkmate after move
            if self.is_checkmate(self.board, self.current_turn):
                print(f"Checkmate! {self.opponent_color(self.current_turn).capitalize()} wins!")
                return True  # You can add logic to end the game here.

            # Switches turns
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        
    def copy_board_from(self, board):
        new_board = [[board[row][col] for col in range(8)] for row in range(8)]
        return new_board
    
    @staticmethod
    def opponent_color(color):
        return 'black' if color == 'white' else 'white'
        
    
    def is_square_attacked(self, board, square, attacker_color):
        '''
        Returns True if the given square is attacled by any piece of attacker_color.
        '''

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == attacker_color:
                    # For pawns, the attack moves.
                    if piece.piece_type == 'Pawn':
                        # Calculates the pawn attack squares
                        pawn_attacks = []
                        for delta in (-1,1):
                            attack_row = row + piece.direction
                            attack_col = col + delta
                            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                                pawn_attacks.append((attack_row, attack_col))
                        if square in pawn_attacks:
                            return True
                    else:
                        # Use the pieces's possible_moves method
                        moves = piece.possible_moves(board, (row, col))
                        if square in moves:
                            return True
        return False
    
    def find_king(self, board, color):
        '''
        Finds and returns the position (row, col) of the king of the given color.
        '''
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.piece_type == 'King' and piece.color == color:
                    return (row, col)
        return None            

    def is_move_valid(self, start, end, current_turn):
        """
        Check if making a move from start to end would leave the current_turn's king in check.
        """ 
        # Creates a deep copy of the board
        temp_board = self.copy_board()
        piece = temp_board[start[0]][start[1]]
        temp_board[end[0]][end[1]] = piece
        temp_board[start[0]][start[1]] = None
        king_pos = self.find_king(temp_board, current_turn)
        # Determines the opponent's color
        attacker_color = 'black' if current_turn == 'white' else 'white'
        return not self.is_square_attacked(temp_board, king_pos, attacker_color) 
    
    def copy_board(self):
        """
        Creates a deep copy of the board state.
        """
        new_board = [[self.board[row][col] for col in range(8)] for row in range(8)]
        return new_board
    
    def is_checkmate(self, board, current_color):
        """
        Returns True if the current player (current_color) is checkmated.
        board: the current board state.
        current_color: 'white' or 'black'.
        """

        # Finds the kings position 
        king_pos = self.find_king(board, current_color)
        if king_pos is None:
            # Edge case, should never happen
            return True

        # If the king is not in check it can not be checkmated
        opponent_color = 'black' if current_color == 'white' else 'white'
        if not self.is_square_attacked(board, king_pos, opponent_color):
            return False
        
        # Generates all legal moves for a player.
        legal_moves_found = False
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == current_color:
                    moves = piece.possible_moves(board, (row, col))
                    for move in moves:
                        # Creates a copy of the board and simulates moves
                        temp_board = self.copy_board_from(self.board)
                        self.simulate_move(temp_board, (row, col), move) 

                        # Finds king new position if it has moved
                        new_king_pos = self.find_king(temp_board, current_color)

                        # If the king is not attacked in the simulation, then a legal move exisit 
                        if not self.is_square_attacked(temp_board, new_king_pos, opponent_color):
                            legal_moves_found = True
                            break
                    if legal_moves_found:
                        break
            if legal_moves_found:
                break
        # If no legal moves saves the king, then its checkmate 
        return not legal_moves_found


    def simulate_move(self, board, start, end):
        """
        Execute a move on the given board (which is a copy) for simulation purposes.
        This should move the piece from start to end and update the board accordingly.
        """
        piece = board[start[0]][start[1]]
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None

        if piece.piece_type == 'King':
            self.king_positions[piece.color] = end


class Piece:
    def __init__(self, piece_type, color, history=None):
        '''
        Initaliase a chess piece

        piece_type - Type of chess piece (e.g., 'King', 'Queen', 'Rook', etc.)
        color - White or Black
        history - list of moves made by the piece 
        '''

        self.piece_type = piece_type
        self.color = color.lower()
        self.history = history if history is not None else []


class Pawn(Piece):
    def __init__(self, color, direction, first_move=True):
        super().__init__(piece_type='Pawn', color=color, history=[])
        self.direction = direction # 1 or -1 based on board position 
        self.first_move = first_move

        
    def possible_moves(self, board, current_position, en_passant=None):
        """
        Calculate and return a list of possible moves for the Pawn.

        
        Parameters:
            board: The current board state (to check occupancy and enemy pieces).
            current_position: The current coordinates of the Pawn.
        
        Returns:
            A list of moves that the Pawn can legally make.
        """

        moves = []
        row, col = current_position

        # one square forward
        one_step = row + self.direction
        if 0 <= one_step < 8: #Ensures we remain on the board
            if board[one_step][col] is None:
                moves.append((one_step, col))

                # Two square forward (only on first move)
                if self.first_move:
                    two_step = row + 2 * self.direction
                    if 0 <= two_step < 8 and board[two_step][col] is None:
                        moves.append((two_step, col))

        # Diagonal captures
        for delta_col in (-1, 1):
            new_col = col + delta_col
            new_row = row + self.direction

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target is not None:
                    if target.color != self.color:
                        moves.append((new_row, new_col))
                else:

                    # En Passant capture
                    if en_passant is not None and en_passant == (new_row, new_col):
                        moves.append((new_row, new_col))

        return moves

class King(Piece):
    def __init__(self, color, first_move=True):
        super().__init__(piece_type='King', color=color)
        self.first_move = first_move

    def possible_moves(self, board, current_position, castle=True):
        """
        Calculate and return a list of possible moves for the King.

        The king can move one step in any direction, as long as it can not be checked on that square 
        The king can also castle on its first move and if there are no squares in can be checked on 

        Parameters:
            board: The current board state (to check occupancy and enemy pieces).
            current_position: The current coordinates of the King.
        
        Returns:
            A list of moves that the King can legally make.



        Tech dept : verify that the king is not currently in check and that none of the squares it crosses are under attack.
                  : The castling logic should also confirm that the relevant rook has not moved. You may need to store that information in your rook subclass or via the board state.
                  : update the first move attribute 
        
        
        """           
        moves = []
        row, col = current_position 

        directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

        for delta_row, delta_col in directions:
            new_row, new_col = row + delta_row, col + delta_col

            # Checks the board boundaries
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_cell = board[new_row][new_col]

                # If target is empty or not occupied by an enemy piece its a legal move
                if target_cell is None or target_cell.color != self.color:
                    moves.append((new_row, new_col))


        # Only considered if king has not moved
        if castle and self.first_move:
            # --- Kingside Castling ---
            # For kingside castling, squares (row, col+1) and (row, col+2) must be empty.
            if col + 2 < 8 and board[row][col+1] is None and board[row][col+2] is None:
                # Check that the rook on the kingside exists and hasn't moved.
                rook = board[row][7]
                if rook is not None and rook.piece_type == 'Rook' and rook.first_move:
                    moves.append((row, col+2))
            # --- Queenside Castling ---
            # For queenside castling, squares (row, col-1), (row, col-2) and (row, col-3) must be empty.
            if col - 3 >= 0 and board[row][col-1] is None and board[row][col-2] is None and board[row][col-3] is None:
                # Check that the rook on the queenside exists and hasn't moved.
                rook = board[row][0]
                if rook is not None and rook.piece_type == 'Rook' and rook.first_move:
                    moves.append((row, col-2))
                    
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(piece_type = 'Queen', color = color)
    
    def possible_moves(self, board, current_position):
        """
        Calculate and return a list of possible moves for the Queen.

        The queen's move generation combines the logic of both the rook and bishop:

        Rook-like movement: Horizontal (left/right) and vertical (up/down).
        Bishop-like movement: Diagonals (up-left, up-right, down-left, down-right).

        Parameters:
            board: The current board state (to check occupancy and enemy pieces).
            current_position: The current coordinates of the Queen.
        
        Returns:
            A list of moves that the Queen can legally make.


        Tech dept : 
        
        """

        moves = []
        row, col = current_position 

        directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)]

        for delta_row, delta_col in directions:
            # Starts stepping from current position 
            new_row, new_col = row + delta_row, col + delta_col

            # Continues in direction until it hits a piece or go's out of board
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    # The square is empty and is a legal move
                    moves.append((new_row, new_col))

                else:
                    # There is a piece on that square
                    if target.color != self.color:
                        # if its an enemy piece 
                        moves.append((new_row, new_col))
                    # Weather its an enemy or not the queen can not move pass this square 
                    break
                # Move one step further in the same direction
                new_row += delta_row 
                new_col += delta_col

        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(piece_type = 'Bishop', color = color)
        """
        Calculate and return a list of legal moves for the Bishop.
        
        Parameters:
            board: The current board state (8x8 grid).
            current_position: A tuple (row, col) representing the Bishop's current position.
        
        Returns:
            A list of tuples, each representing a legal destination for the Bishop.
        """


    def possible_moves(self, board, current_position):
        moves = []
        row, col = current_position

        diagnol_moves = [(-1, -1), (-1, 1),
                         (1, -1), (1, 1)]

        for delta_row, delta_col in diagnol_moves:
            # starts stepping from current 
            new_row, new_col = row + delta_row, col + delta_col

            # Continues in  direction until it hits a piece or gos out of bound
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    # The square is empty meaning its a legal move
                    moves.append((new_row, new_col))

                else:
                    # There is a piece on that square
                    if target.color != self.color:
                        # If its an enemy square the bishop can take
                        moves.append((new_row, new_col))
                    # Wheather its an enemy or not the bishop can not move pass this square 
                    break
                # Move one step further in the same direction
                new_row += delta_row 
                new_col += delta_col

        return moves
                    
class Rook(Piece):
    def __init__(self, color, first_move=True):
        super().__init__(piece_type='Rook', color=color)
        self.first_move = first_move

    def possible_moves(self, board, current_position):
        moves = []
        row, col = current_position

        bishop_moves = [
               (-1, 0),
        (0, -1),    (0, 1),
               (1, 0)
        ]

        for delta_row, delta_col in bishop_moves:
            # starts stepping from current position
            new_row, new_col = row + delta_row, col + delta_col

            # Continues in directoin untill it hits a piece or gos out of bound
            while 0<= new_row < 8 and 0<= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))

                else:
                    if target.color != self.color:
                        moves.append((new_row, new_col))
                    break
                new_row += delta_row
                new_col += delta_col
        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(piece_type='Knight', color=color)

    def possible_moves(self, board, current_position):
        moves = []
        row, col = current_position
        knight_moves = [(2, 1),(2, -1),(-2, 1),(-2, -1),(1, 2),(1, -2),(-1, 2),(-1, -2),]

        for delta_row, delta_col in knight_moves:
            new_row = row + delta_row
            new_col = col + delta_col

            # Checks if current position is within the board boundaries 
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                # The move is only valid if its on the board and if the square is empty or occupied by an enemy
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))

        return moves

if __name__ == '__main__':
    game = Game()
    game.start()

