import copy
from typing import List, Tuple, NamedTuple




class Checkers:


    class Pair(NamedTuple):
        row: int
        col: int

        def __add__(self, other: "Pair") -> "Pair":
            return Checkers.Pair(self.row + other.row, self.col + other.col)

        def __sub__(self, other: "Pair") -> "Pair":
            return Checkers.Pair(self.row - other.row, self.col - other.col)

        def is_jump(self) -> bool:
            return abs(self.row) == 2 and abs(self.col) == 2

        def is_move(self) -> bool:
            return abs(self.row) == 1 and abs(self.col) == 1


    class MoveOutcome(NamedTuple):
        success: bool
        promoted: bool
        location: "Pair"


    class Move(NamedTuple):
        row: int
        col: int






    default_board = [
        [0, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, -1, 0, -1, 0, -1, 0],
        [0, -1, 0, -1, 0, -1, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]

    black_moves = [Pair(-1, -1), Pair(-1, 1)]
    black_jumps = [Pair(-2, -2), Pair(-2, 2)]

    white_moves = [Pair(1, -1), Pair(1, 1)]
    white_jumps = [Pair(2, -2), Pair(2, 2)]

    king_moves = [Pair(-1, -1), Pair(-1, 1), Pair(1, -1), Pair(1, 1)]
    king_jumps = [Pair(-2, -2), Pair(-2, 2), Pair(2, -2), Pair(2, 2)]

    black = 1
    white = -1
    black_king = 2
    white_king = -2
    empty = 0
    size = 8


    def __init__(self, board: List[List[int]] = default_board) -> None:
        self.board = copy.deepcopy(board)
        self.black_score = 0
        self.white_score = 0
        self.black_count = 12
        self.white_count = 12


    def __repr__(self) -> str:
        return '\n'.join([f"\t" + ' '.join([str(cell) for cell in line]) for line in self.board]) #might wanna print scores


    def get_white_count(self) -> int:
        return self.white_count


    def get_black_count(self) -> int:
        return self.black_count


    def is_white(self, pawn: int) -> bool:
        return pawn < 0


    def is_black(self, pawn: int) -> bool:
        return pawn > 0

    
    def is_king(self, pawn: int) -> bool:
        return abs(pawn) == 2


    def are_enemies(self, lhs: int, rhs: int) -> bool:
        return lhs ^ rhs < 0


    def can_promote(self, origin: Pair) -> bool:
        pawn = self.board[origin.row][origin.col]

        if pawn == Checkers.empty:
            return False #spot is empty

        if self.is_king(pawn):
            return False #already promoted

        if self.is_black(pawn):
            if origin.row == 0:
                return True #can promote at row 0
        elif self.is_white(pawn):
            if origin.row == Checkers.size - 1:
                return True #can promote at row size - 1


    def promote(self, origin: Pair) -> bool: #returns the value of can_promote()
        if not self.can_promote(origin):
            return False

        self.board[origin.row][origin.col] *= 2

        #increase the player's score
        pawn = self.board[origin.row][origin.col]
        if self.is_black(pawn):
            self.black_score += 1
        elif self.is_white(pawn):
            self.white_score -= 1

        return True


    def get_moves(self, pawn: int) -> List[Pair]:
        if pawn == Checkers.black:
            return Checkers.black_moves
        elif pawn == Checkers.white:
            return Checkers.white_moves
        elif self.is_king(pawn):
            return Checkers.king_moves
        else:
            return []


    def get_jumps(self, pawn: int) -> List[Pair]:
        if pawn == Checkers.black:
            return Checkers.black_jumps
        elif pawn == Checkers.white:
            return Checkers.white_jumps
        elif self.is_king(pawn):
            return Checkers.king_jumps
        else:
            return []


    def valid_move(self, origin: Pair, move: Pair) -> None:
        if not (0 <= origin.col + move.col < Checkers.size and 0 <= origin.row + move.row < Checkers.size):
            return False #list index out of range

        pawn = self.board[origin.row][origin.col]
        spot = self.board[origin.row + move.row][origin.col + move.col]

        if pawn == Checkers.empty:
            #print("uwu")
            return False #attempts to move nothing

        if spot != Checkers.empty:
            return False #spot already taken

        #origin is a pawn and the location is empty, assert if the pawn can move in that direction
        valid_moves = self.get_moves(pawn)

        if move in valid_moves:
            return True
        else:
            return False


    def move(self, origin: Pair, move: Pair) -> MoveOutcome: #returns the value of valid_move()
        if not self.valid_move(origin, move):
            return (False, False)

        #move is valid, apply it
        self.board[origin.row + move.row][origin.col + move.col] = self.board[origin.row][origin.col]
        self.board[origin.row][origin.col] = Checkers.empty

        #promote if needed
        promoted = self.promote(Checkers.Pair(origin.row + move.row, origin.col + move.col)) #we could return this as well

        return (True, promoted)


    def valid_jump(self, origin: Pair, jump: Pair) -> bool:
        if not (0 <= origin.col + jump.col < Checkers.size and 0 <= origin.row + jump.row < Checkers.size):
            return False #list index out of range

        pawn = self.board[origin.row][origin.col]
        spot = self.board[origin.row + jump.row][origin.col + jump.col]
        jumped_piece = self.board[origin.row + int(jump.row/2)][origin.col + int(jump.col/2)]

        if pawn == Checkers.empty:
            return False #attempts to move nothing

        if spot != Checkers.empty:
            return False #spot already taken

        if jumped_piece == Checkers.empty:
            return False #attempts to jump nothing

        if not self.are_enemies(pawn, jumped_piece):
            return False #cant jump this piece

        #origin is a pawn and the location is empty, jumped piece is also an enemy, assert if the pawn can jump in that direction
        valid_jumps = self.get_jumps(pawn)

        if jump in valid_jumps:
            return True
        else:
            return False


    def jump(self, origin: Pair, jump: Pair) -> MoveOutcome: #returns the value of valid_jump() and whether the pawn promoted or not
        if not self.valid_jump(origin, jump):
            return (False, False)

        #jump is valid, apply it
        enemy_pawn = self.board[origin.row + int(jump.row/2)][origin.col + int(jump.col/2)] #store the enemy pawn
        self.board[origin.row + int(jump.row/2)][origin.col + int(jump.col/2)] = Checkers.empty #eliminate piece
        self.board[origin.row + jump.row][origin.col + jump.col] = self.board[origin.row][origin.col] #set new spot to pawn
        self.board[origin.row][origin.col] = Checkers.empty #set old spot to empty

        #decrease enemy's score and count
        if self.is_black(enemy_pawn):
            self.black_score -= enemy_pawn
            self.black_count -= 1
        elif self.is_white(enemy_pawn):
            self.white_score -= enemy_pawn
            self.white_count -= 1

        promoted = self.promote(Checkers.Pair(origin.row + jump.row, origin.col + jump.col)) #we could return this as well

        return (True, promoted)


    def get_valid_moves(self, origin: Pair) -> List[Pair]:
        valid_moves = []
        moves = self.get_moves(self.board[origin.row][origin.col])

        for move in moves:
            if self.valid_move(origin, move):
                valid_moves.append(move)

        return valid_moves


    def get_valid_jumps(self, origin: Pair) -> List[Pair]:
        valid_jumps = []
        jumps = self.get_jumps(self.board[origin.row][origin.col])

        for jump in jumps:
            if self.valid_jump(origin, jump):
                valid_jumps.append(jump)

        return valid_jumps


    def get_all_white_moves(self) -> List[Tuple[Pair, List[Pair]]]:
        all_moves = []

        for i, row in enumerate(self.board):
            for j, pawn in enumerate(row):
                if self.is_white(pawn):
                    origin = Checkers.Pair(i, j)
                    moves = self.get_valid_moves(origin)
                    if moves:
                        all_moves.append((origin, moves))

        return all_moves


    def get_all_black_moves(self) -> List[Tuple[Pair, List[Pair]]]:
        all_moves = []

        for i, row in enumerate(self.board):
            for j, pawn in enumerate(row):
                if self.is_black(pawn):
                    origin = Checkers.Pair(i, j)
                    moves = self.get_valid_moves(origin)
                    if moves:
                        all_moves.append((origin, moves))

        return all_moves


    def get_all_white_jumps(self) -> List[Tuple[Pair, List[Pair]]]:
        all_jumps = []

        for i, row in enumerate(self.board):
            for j, pawn in enumerate(row):
                if self.is_white(pawn):
                    origin = Checkers.Pair(i, j)
                    jumps = self.get_valid_jumps(origin)
                    if jumps:
                        all_jumps.append((origin, jumps))

        return all_jumps


    def get_all_black_jumps(self) -> List[Tuple[Pair, List[Pair]]]:
        all_jumps = []

        for i, row in enumerate(self.board):
            for j, pawn in enumerate(row):
                if self.is_black(pawn):
                    origin = Checkers.Pair(i, j)
                    jumps = self.get_valid_jumps(origin)
                    if jumps:
                        all_jumps.append((origin, jumps))

        return all_jumps


    def get_black_score(self) -> int: #sum of all pieces
        return self.black_score


    def get_white_score(self) -> int: #sum of all pieces
        return self.white_score


    def get_score(self, player: int) -> int:
        if self.is_white(player):
            return self.white_score
        else:
            return self.black_score


    def can_move(self, player: int) -> bool: #this is just get_all_player_jumps() except it halts on failure
        for i, row in enumerate(self.board):
            for j, pawn in enumerate(row):
                if not self.are_enemies(pawn, player):
                    if self.get_valid_jumps(Checkers.Pair(i, j)):
                        #there are available jumps, therefore player cannot move
                        return False

        return True


    def white_won(self) -> bool:
        return self.black_count == 0


    def black_won(self) -> bool:
        return self.white_count == 0


    def won(self, player) -> bool:
        if self.black_count == 0:
            return Checkers.black
        elif self.white_count == 0:
            return Checkers.white
        else:
            return None


    #def get_jump_sequences(self) -> List[Jump_seq]:

