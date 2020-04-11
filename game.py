from checkers import *
from math import inf


class Game:

    def __init__(self) -> None:
        self.board = Checkers([
            # a    b    c    d    e    f    g    h
            [0, -1, 0, -1, 0, -1, 0, -1],   #0
            [-1, 0, -1, 0, -1, 0, -1, 0],   #1
            [0, -1, 0, -1, 0, -1, 0, -1],   #2
            [0, 0, 0, 0, 0, 0, 0, 0],   #3
            [0, 0, 0, 0, 0, 0, 0, 0],   #4
            [1, 0, 1, 0, 1, 0, 1, 0],   #5
            [0, 1, 0, 1, 0, 1, 0, 1],   #6
            [1, 0, 1, 0, 1, 0, 1, 0]    #7
        ])


    def __repr__(self) -> str:
        return str(self.board)


    def on(self) -> bool:
        return True


    def parse_input(self, turn: str) -> Tuple[Pair, Pair]:
        turn = turn.split(' ')
        origin = Pair(int(turn[0][0]), ord(turn[0][1]) - 97)
        move = Pair(int(turn[1][0]) - origin.row, ord(turn[1][1]) - 97 - origin.col)

        return (origin, move)


    def human_turn(self) -> None:
        turn = None
        can_move = self.board.can_move(Checkers.black)

        if self.board.can_move(Checkers.black):
            print("You do not have available jumps.")
            while True:
                origin, move = self.parse_input(input("Move: "))

                if self.board.move(origin, move)[0]:
                    break
                else:
                    print("Move was not valid.")    

        else:
            print("You have available jumps.")

            origin = None
            promoted = None

            while True:
                #first prompt, let the user know he must choose a pawn to jump

                origin, jump = self.parse_input(input("Jump: "))

                success, promoted = self.board.jump(origin, jump)

                if success:
                    break
                else:
                    print("Your input was invalid.")

            origin += jump

            while self.board.get_valid_jumps(origin):
                #second prompt, after a succesful jump, notify the user which pawn he must jump
                print(self)

                while True:
                    jump = input("Continue jump using pawn X to: ")
                    jump = Pair(int(jump[0][0]) - origin.row, ord(jump[0][1]) - 97 - origin.col)

                    success, promoted = self.board.jump(origin, jump)

                    if success:
                        break
                    else:
                        print("Your input was invalid.")

                if promoted:
                    break
                else:
                    origin += jump


    def pc_turn(self) -> None:
        #apply minimax
        origin, move = self.get_best_move()[-2:]
        print("pc moved:")
        print(origin, move)
        if abs(move.row) == 2 or abs(move.col) == 2:
            print("ok...")
            print(self.board.jump(origin, move))
        else:
            print(self.board.move(origin, move))


    def turn(self, player: bool) -> None:
        if player:
            self.human_turn()
        else:
            self.pc_turn()


    def get_best_move(self) -> Tuple[Pair, Pair]:
        value, origin, move = self.minimax(self.board, Checkers.white, 5)

        return (origin, move)


    def minimax(self, board: Checkers, player: int, depth: int, jump_lock: Pair = None) -> List[int]: #returns best move/jump
        if board.get_white_count() == 0:
            return [-inf, None, None] #absolute loss

        if board.get_black_count() == 0:
            return [inf, None, None] #absolute win

        if depth == 0:
            return [board.get_score(player) - board.get_score(-player), None, None] #return heuristic value of leaf node

        if player == Checkers.white: #pc, maximizes
            value = -inf

            if jump_lock:
                #we're stuck in a jump sequence
                jumps = board.get_valid_jumps(jump_lock) #compute the available jumps for this pawn

                if jumps:
                    #we have available jumps, continue the jump sequence
                    best_jump = None
                    for jump in jumps:
                        #generate the new board configuration
                        new_board = copy.deepcopy(board)
                        promoted = new_board.jump(jump_lock, jump)[1]

                        if promoted:
                            #end the jump sequence
                            path_value = self.minimax(new_board, Checkers.black, depth - 1)[0]
                        else:
                            #continue jump sequence
                            path_value = self.minimax(new_board, Checkers.white, depth, jump_lock + jump)[0]

                        #check if the computed path is worth it
                        if path_value > value:
                            value = path_value
                            best_jump = jump

                    #we iterated all of the available jumps, return the best
                    return [value, jump_lock, best_jump]     

                else:
                    #we dont have any available jumps
                    #turn to the other player
                    return self.minimax(board, Checkers.black, depth - 1)

            else:

                jumps = board.get_all_white_jumps()

                if jumps:
                    best_jump = None
                    best_origin = None
                    #we have available jumps
                    for origin, jumplist in jumps:
                        for jump in jumplist:
                            #generate the new board configuration
                            new_board = copy.deepcopy(board)
                            promoted = new_board.jump(origin, jump)[1]

                            if promoted:
                                #doesnt enter a jump sequence
                                path_value = self.minimax(new_board, Checkers.black, depth - 1)[0]
                            else:
                                #we enter a POSSIBLE jump sequence
                                path_value = self.minimax(new_board, Checkers.white, depth, origin + jump)[0]

                            #check if the computed path is worth it
                            if path_value > value:
                                value = path_value
                                best_jump = jump
                                best_origin = origin

                    #we iterated all of the available jumps, return the best
                    return [value, best_origin, best_jump]
                else:
                    best_move = None
                    best_origin = None
                    #no jumps available, iterate the possible moves
                    moves = board.get_all_white_moves()
                    for origin, movelist in moves:
                        for move in movelist:
                            #generate the new board configuration
                            new_board = copy.deepcopy(board)
                            new_board.move(origin, move)

                            path_value = self.minimax(new_board, Checkers.black, depth - 1)[0]
                            
                            #check if the computed path is worth it
                            if path_value > value:
                                value = path_value
                                best_move = move
                                best_origin = origin

                    #we iterated all of the available moves, return the best
                    return [value, best_origin, best_move]

        elif player == Checkers.black:
            value = inf

            if jump_lock:
                #we're stuck in a jump sequence
                jumps = board.get_valid_jumps(jump_lock) #compute the available jumps for this pawn

                if jumps:
                    #we have available jumps, continue the jump sequence
                    best_jump = None
                    for jump in jumps:
                        #generate the new board configuration
                        new_board = copy.deepcopy(board)
                        promoted = new_board.jump(origin, jump)[1]

                        if promoted:
                            #end the jump sequence
                            path_value = self.minimax(new_board, Checkers.white, depth - 1)[0]
                        else:
                            #continue jump sequence
                            path_value = self.minimax(new_board, Checkers.black, depth, origin + jump)[0]

                        #check if the computed path is worth it
                        if path_value < value:
                            value = path_value
                            best_jump = jump

                    #we iterated all of the available jumps, return the best
                    return [value, jump_lock, best_jump]     

                else:
                    #we dont have any available jumps
                    #turn to the other player
                    return self.minimax(board, Checkers.white, depth - 1)

            else:

                jumps = board.get_all_white_jumps()

                if jumps:
                    best_jump = None
                    best_origin = None
                    #we have available jumps
                    for origin, jumplist in jumps:
                        for jump in jumplist:
                            #generate the new board configuration
                            new_board = copy.deepcopy(board)
                            promoted = new_board.jump(origin, jump)[1]

                            if promoted:
                                #doesnt enter a jump sequence
                                path_value = self.minimax(new_board, Checkers.white, depth - 1)[0]
                            else:
                                #we enter a POSSIBLE jump sequence
                                path_value = self.minimax(new_board, Checkers.black, depth, origin + jump)[0]

                            #check if the computed path is worth it
                            if path_value < value:
                                value = path_value
                                best_jump = jump
                                best_origin = origin

                    #we iterated all of the available jumps, return the best
                    return [value, best_origin, best_jump]
                else:
                    best_move = None
                    best_origin = None
                    #no jumps available, iterate the possible moves
                    moves = board.get_all_white_moves()
                    for origin, movelist in moves:
                        for move in movelist:
                            #generate the new board configuration
                            new_board = copy.deepcopy(board)
                            new_board.move(origin, move)

                            path_value = self.minimax(new_board, Checkers.white, depth - 1)[0]
                            
                            #check if the computed path is worth it
                            if path_value < value:
                                value = path_value
                                best_move = move
                                best_origin = origin

                    #we iterated all of the available moves, return the best
                    return [value, best_origin, best_move]