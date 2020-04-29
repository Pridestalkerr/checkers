import copy
from typing import List, Tuple, NamedTuple, Union, Set




class Checkers:

    # ------------------
    # NAMESPACED CLASSES
    # ------------------

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


    class Location(Pair):
        pass


    class Move(Pair):
        pass

    
    class Jump(Pair):
        pass


    class Move_outcome(NamedTuple):
        success: bool
        promoted: bool
        location: "Location"


    # just an alias
    Pawn_type = int


    class Pawn(NamedTuple):
        location: "Location"
        pawn_type: "Pawn_type"


    Player = int



    # ----------------
    # STATIC VARIABLES
    # ----------------

    default_board = [
        [0, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, -1, 0, -1, 0, -1, 0],
        [0, -1, 0, -1, 0, -1, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [-1, 0, 0, 0, 0, 0, 0, 0],
        # [0, +1, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, +1, 0, +1, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0],
        # [0, +1, 0, +1, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    black_moves = [Move(-1, -1), Move(-1, 1)]
    black_jumps = [Move(-2, -2), Move(-2, 2)]

    white_moves = [Move(1, -1), Move(1, 1)]
    white_jumps = [Move(2, -2), Move(2, 2)]

    king_moves = [Move(-1, -1), Move(-1, 1), Move(1, -1), Move(1, 1)]
    king_jumps = [Move(-2, -2), Move(-2, 2), Move(2, -2), Move(2, 2)]

    black = 1
    white = -1
    black_king = 3
    white_king = -3
    empty = 0
    size = 8



    # ----------------
    # PUBLIC FUNCTIONS
    # ----------------

    def __init__(self, board: List[List[int]] = default_board) -> None:
        self.board = copy.deepcopy(board)
        self.white_score = 0
        self.black_score = 0
        self.white_count = 12
        self.black_count = 12
        self.white_kings_count = 0
        self.black_kings_count = 0


    def __repr__(self) -> str:
        # might wanna print scores
        return '\n'.join([f"\t" + ' '.join([str(cell) for cell in line]) for line in self.board])


    def get_white_count(self) -> int:
        return self.white_count


    def get_black_count(self) -> int:
        return self.black_count


    def get_count(self, player: Pawn_type) -> int:
        if player == Checkers.white:
            return self.get_white_count()
        elif player == Checkers.black:
            return self.get_black_count()
        else:
            raise Exception("Invalid player.")


    def get_white_kings_count(self) -> int:
        return self.white_kings_count


    def get_black_kings_count(self) -> int:
        return self.black_kings_count


    def get_kings_count(self, player: Pawn_type) -> int:
        if player == Checkers.white:
            return self.get_white_kings_count()
        elif player == Checkers.black:
            return self.get_black_kings_count()
        else:
            raise Exception("Invalid player.")


    # type assessments

    def is_white(self, location: Location) -> bool:
        return self.board[location.row][location.col] < 0


    def is_white_pawn(self, location: Location) -> bool:
        return self.board[location.row][location.col] == -1


    def is_white_king(self, location: Location) -> bool:
        return self.board[location.row][location.col] == -3


    def is_black(self, location: Location) -> bool:
        return self.board[location.row][location.col] > 0


    def is_black_pawn(self, location: Location) -> bool:
        return self.board[location.row][location.col] == 1


    def is_black_king(self, location: Location) -> bool:
        return self.board[location.row][location.col] == 3


    def is_pawn(self, location: Location) -> bool:
        return abs(self.board[location.row][location.col]) == 1


    def is_king(self, location: Location) -> bool:
        return abs(self.board[location.row][location.col]) == 3


    def are_enemies(self, lhs: int, rhs: int) -> bool:
        return self.board[lhs.row][lhs.col] ^ self.board[rhs.row][rhs.col] < 0


    def is_empty(self, location: Location) -> bool:
        return self.board[location.row][location.col] == 0


    def won(self) -> int:
        if self.black_count == 0:
            return Checkers.black
        elif self.white_count == 0:
            return Checkers.white
        else:
            return None


    # promotion logic

    def can_promote(self, location: Location) -> bool:
        location_type = self.board[location.row][location.col]

        if location_type == Checkers.empty:
            #spot is empty
            return False 

        if self.is_king(location):
            #already promoted
            return False

        if self.is_black(location) and location.row == 0:
            #black promotes at row 0
            return True

        if self.is_white(location) and location.row == Checkers.size - 1:
            #can promote at row size - 1
            return True


    # returns the value of self.can_promote()
    def promote(self, location: Location) -> bool:
        if not self.can_promote(location):
            return False

        # increase the value of the pawn
        self.board[location.row][location.col] *= 3

        # increase the player's score
        if self.is_black(location):
            self.black_score += 3
        else:
            self.white_score += 3

        return True


    # move logic

    def valid_move(self, location: Location, move: Move) -> bool:
        destination = location + move
        if not (0 <= destination.row < Checkers.size and 0 <= destination.col < Checkers.size):
            # list index of destination is out of range
            return False

        destination_type = self.board[destination.row][destination.col]
        location_type = self.board[location.row][location.col]

        if location_type == Checkers.empty:
            # attempts to move nothing
            return False

        if destination_type != Checkers.empty:
            # attempted destination is not empty
            return False

        # location is a pawn and the destination is empty,
        # assert if the pawn can move in that direction
        if move in self.get_possible_moves(location):
            return True
        else:
            return False


    def move(self, location: Location, move: Move) -> Move_outcome:
        if not self.valid_move(location, move):
            return (False, False)

        destination = location + move

        # move is valid, apply it
        self.board[destination.row][destination.col] = self.board[location.row][location.col]
        self.board[location.row][location.col] = Checkers.empty

        # promote if needed
        promoted = self.promote(destination)

        return (True, promoted)


    # jump logic

    def valid_jump(self, location: Location, jump: Move) -> bool:
        destination = location + jump
        if not (0 <= destination.row < Checkers.size and 0 <= destination.col < Checkers.size):
            # list index of destination is out of range
            return False

        destination_type = self.board[destination.row][destination.col]
        location_type = self.board[location.row][location.col]
        jumped = Checkers.Location(location.row + int(jump.row/2), location.col + int(jump.col/2))
        jumped_type = self.board[jumped.row][jumped.col]

        if location_type == Checkers.empty:
            # attempts to move nothing
            return False

        if destination_type != Checkers.empty:
            # attempted destination is not empty
            return False

        if jumped_type == Checkers.empty:
            # attempts to jump over nothing
            return False

        if not self.are_enemies(location, jumped):
            # attempts to jump over ally
            return False

        # location is a pawn and the destination is empty,
        # jumped piece is also an enemy,
        # assert if the pawn can jump in that direction
        if jump in self.get_possible_jumps(location):
            return True
        else:
            return False


    def jump(self, location: Location, jump: Move) -> Move_outcome:
        if not self.valid_jump(location, jump):
            return (False, False)

        destination = location + jump
        jumped = Checkers.Location(location.row + int(jump.row/2), location.col + int(jump.col/2))
        jumped_type = self.board[jumped.row][jumped.col]

        # jump is valid, apply it
        self.board[jumped.row][jumped.col] = Checkers.empty    # eliminate piece
        self.board[destination.row][destination.col] = self.board[location.row][location.col]    # move the piece
        self.board[location.row][location.col] = Checkers.empty    # set old spot to empty

        # increase player score and decrease enemy counts
        if self.is_black(destination):
            self.black_score += jumped_type
            self.white_count -= 1
            if self.is_king(jumped):
                self.white_kings_count -= 1
        else:
            self.white_score += jumped_type
            self.black_count -= 1
            if self.is_king(jumped):
                self.black_kings_count -= 1

        # promote if needed
        promoted = self.promote(destination)

        return (True, promoted)


    def apply_jump_sequence(self, location: Location, seq: List[Jump]) -> Move_outcome:
        for jump in seq:
            self.jump(location, jump)
            location += jump

        promoted = self.promote(location)

        return (True, promoted)





    def get_moves(self, location: Location = None, player: Player = None) -> Union[List[Move], List[Tuple[Location, List[Move]]]]:
        if location:
            # get moves for the specified location
            return self.get_moves_for_pawn(location)
        elif player:
            # get moves for all pawns
            return self.get_moves_for_player(player)
        else:
            raise Exception("Invalid keyword arguments.")


    def get_jumps(self, location: Location = None, player: Player = None, recursive: bool = False) -> Union[List[Jump], List[Tuple[Location, List[Jump]]]]:
        if location:
            # get moves for the specified location
            return self.get_jump_sequences_for_pawn(location) if recursive else self.get_jumps_for_pawn(location)
        elif player:
            # get moves for all pawns
            return self.get_jump_sequences_for_player(player) if recursive else self.get_jumps_for_player(player)
        else:
            raise Exception("Invalid keyword arguments.")


    def apply(self, location: Location, action: Union[Move, Jump]) -> Move_outcome:
        if type(action) == Checkers.Move:
            return self.move(location, action)
        elif type(action) == Checkers.Jump:
            return self.jump(location, action)
        elif type(action) == list:
            for jump in action:
                self.jump(location, jump)
                location += jump
        else:
            raise Exception("Invalid action type.")









    # PRIVATE GETTERS

    def get_moves_for_pawn(self, location: Location) -> List[Move]:
        valid_moves = []
        possible_moves = self.get_possible_moves(location)

        for move in possible_moves:
            if self.valid_move(location, move):
                valid_moves.append(move)

        return valid_moves


    def get_jumps_for_pawn(self, location: Location) -> List[Jump]:
        valid_jumps = []
        possible_jumps = self.get_possible_jumps(location)

        for jump in possible_jumps:
            if self.valid_jump(location, jump):
                valid_jumps.append(jump)

        return valid_jumps


    def get_moves_for_player(self, player: Player) -> List[Tuple[Location, List[Move]]]:
        if player == Checkers.black:
            type_assessment = self.is_black
        elif player == Checkers.white:
            type_assessment = self.is_white
        else:
            raise Exception("Invalid player argument.")

        player_moves = []

        for i, row in enumerate(self.board):
            for j, location_type in enumerate(row):
                location = Checkers.Location(i, j)
                if type_assessment(location):
                    moves = self.get_moves_for_pawn(location)
                    if moves:
                        player_moves.append((location, moves))

        return player_moves


    def get_jumps_for_player(self, player: Player) -> List[Tuple[Location, List[Jump]]]:
        if player == Checkers.black:
            type_assessment = self.is_black
        elif player == Checkers.white:
            type_assessment = self.is_white
        else:
            raise Exception("Invalid player argument.")

        player_jumps = []

        for i, row in enumerate(self.board):
            for j, location_type in enumerate(row):
                location = Checkers.Location(i, j)
                if type_assessment(location):
                    jumps = self.get_jumps_for_pawn(location)
                    if jumps:
                        player_jumps.append((location, jumps))

        return player_jumps




    # instead of generating new boards everytime, we will keep a list of pawns that have been removed from the game,
    # we can then check if the play a role in the current iteration's attempts and act accordingly
    def get_jump_sequences_for_pawn(self, location: Location) -> List[List[Jump]]:
        seqs = []

        for jump in self.get_jumps_for_pawn(location):
            new_board = copy.deepcopy(self)
            _, promoted = new_board.jump(location, jump)

            if promoted:
                return [[jump]]

            ret = new_board.get_jump_sequences_for_pawn(location + jump)
            if ret:
                for seq in ret:
                    seq.insert(0, jump)
                
                seqs.extend(ret)
            else:
                seqs.append([jump])


        return seqs






    # #[ (location, [ jump_sequence ] ) ]
    def get_jump_sequences_for_player(self, player: Player) -> List[Tuple[Location, List[List[Jump]]]]:
        if player == Checkers.black:
            type_assessment = self.is_black
        elif player == Checkers.white:
            type_assessment = self.is_white
        else:
            raise Exception("Invalid player argument.")

        player_seqs = []

        for i, row in enumerate(self.board):
            for j, location_type in enumerate(row):
                location = Checkers.Location(i, j)
                if type_assessment(location):
                    jumps = self.get_jump_sequences_for_pawn(location)
                    if jumps:
                        player_seqs.append((location, jumps))

        return player_seqs





    # DEPRECATED, FIX THESE, MAKE A PAWN CLASS

    def get_possible_moves(self, location: Location) -> List[Move]:
        if self.is_black_pawn(location):
            return Checkers.black_moves
        elif self.is_white_pawn(location):
            return Checkers.white_moves
        elif self.is_king(location):
            return Checkers.king_moves
        else:
            raise Exception("Invalid location type.")


    def get_possible_jumps(self, location: Location) -> List[Jump]:
        if self.is_black_pawn(location):
            return Checkers.black_jumps
        elif self.is_white_pawn(location):
            return Checkers.white_jumps
        elif self.is_king(location):
            return Checkers.king_jumps
        else:
            raise Exception("Invalid location type.")
