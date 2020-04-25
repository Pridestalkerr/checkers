import pygame

from typing import List, Tuple, NamedTuple

from checkers import *
from gameui import *

from math import inf

import threading



class Game:


    def __init__(self, display_width: int = 900, display_height: int = 900,
                 cell_width: int = 100, cell_height: int = 100, border_size: int = 0,
                 background_color: (int, int, int) = (0, 0, 0),
                 border_color: (int, int, int) = (0, 0, 0),
                 black_cell_color: (int, int, int) = (0, 0, 0),
                 white_cell_color: (int, int, int) = (255, 255, 255),
                 font_color: (int, int, int) = (255, 255, 255),
                 black_sprite: str = "black.png", black_king_sprite: str = "black_king.png", 
                 white_sprite: str = "white.png", white_king_sprite: str = "white_king.png",
                 caption: str = "Checkers",
                 logo: str = "logo.png",
                 auto_init: bool = True
    ) -> None:

        self.board = Checkers()

        self.ui = GameUI(background_color = background_color, border_color = border_color, black_cell_color = black_cell_color, white_cell_color = white_cell_color, border_size = border_size, auto_init = False)

        #self.cli = Gamecli()



    # wrapper for a default game\
    def run(self) -> None:

        self.ui.init_window()
        self.ui.draw(self.board)
        self.ui.update()

        run = True
        selected = None #for mouse moves
        force_pawn = None #for jump seq
        player = True
        pc_thread = None

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if player:
                        pos = self.ui.mapCoordToIndex(*pygame.mouse.get_pos())

                        if selected:
                            attempt = Checkers.Pair(*pos) - Checkers.Pair(*selected)
                            if attempt.is_move():
                                self.board.move(Checkers.Pair(*selected), attempt)
                            else:
                                self.board.jump(Checkers.Pair(*selected), attempt)
                                if self.won() != None:
                                    #player won with a jump
                                    self.ui.draw_winner("black")
                                    self.ui.update()


                            #self.ui.remove_pawn(*Checkers.Pair(*selected))
                            selected = None
                            player = False
                            pc_thread = threading.Thread(target = self.pc_turn, daemon = True)
                            pc_thread.start()
                        else:
                            selected = pos

            if not player:
                if pc_thread.is_alive():
                    pass
                else:
                    pc_thread.join()
                    player = True
                    if self.won() != None:
                        # pc won with a jump
                        self.ui.draw_winner("pc")
                        self.ui.update()


            
            self.ui.display.fill((0, 0, 0))
            self.ui.draw(self.board)
            self.ui.update()
            self.ui.clock.tick(30)



        pygame.quit()




    def won(self) -> bool:
        if self.board.white_count == 0:
            return True # black wins
        if self.board.black_count == 0:
            return False # white wins

        return None
        

    def player_turn(self) -> None:
        if self.board.can_move(Checkers.black):
            #the player has to move
            pass
        else:
            #the player has to jump
            pass


    def pc_turn(self) -> None:
        #apply minimax
        origin, move = self.get_best_move()[-2:]
        print("pc moved:")
        print(origin, move)
        if abs(move.row) == 2 or abs(move.col) == 2:
            print(self.board.jump(origin, move))
        else:
            print(self.board.move(origin, move))


    def turn(self, player: bool) -> None:
        if player:
            self.human_turn()
        else:
            self.pc_turn()


    def get_best_move(self) -> Tuple[Checkers.Pair, Checkers.Pair]:
        value, origin, move = self.minimax(self.board, Checkers.white, 6)

        return (origin, move)


    def minimax(self, board: Checkers, player: int, depth: int, jump_lock: Checkers.Pair = None) -> List[int]: #returns best move/jump
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
                        promoted = new_board.jump(jump_lock, jump)[1]

                        if promoted:
                            #end the jump sequence
                            path_value = self.minimax(new_board, Checkers.white, depth - 1)[0]
                        else:
                            #continue jump sequence
                            path_value = self.minimax(new_board, Checkers.black, depth, jump_lock + jump)[0]

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

                jumps = board.get_all_black_jumps()

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
                    moves = board.get_all_black_moves()
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



    # def alpha_beta(self, board: Checkers, player: int, depth: int, alpha: int = -inf, beta: int = inf, jump_lock: Checkers.Pair = None) -> (int, int, int): # returns best move/jump?:
    #     if board.get_white_count() == 0:
    #         return (-inf, None, None) #absolute loss

    #     if board.get_black_count() == 0:
    #         return (inf, None, None) #absolute win

    #     if depth == 0:
    #         return (self.heuristic(board), None, None) #return heuristic value of leaf node


    #     # prioritize moves that end in a promotion, requires some sorting of sort,
    #     # must check if sorting on every node is better than pruning (it should be for huge depths)


    #     if player == Checkers.white:
    #         # pc, maximizes
    #         best_option = -inf
    #         extrema = max
    #     elif player == Checkers.black:
    #         # player, minimizes
    #         best_option = inf
    #         extrema = min

    #     # smart man
    #     if jump_lock:
    #         #we're stuck in a jump sequence
    #         jumps = board.get_valid_jumps(jump_lock) #compute the available jumps for this pawn

    #         if jumps:
    #             #we have available jumps, continue the jump sequence
                
    #             for jump in jumps:
    #                 #generate the new board configuration
    #                 new_board = copy.deepcopy(board)
    #                 if new_board.jump(jump_lock, jump).promoted:
    #                     #end the jump sequence
    #                     path = self.minimax(new_board, -player, depth - 1)
    #                 else:
    #                     #continue jump sequence, do not decrease depth
    #                     path = self.minimax(new_board, player, depth, jump_lock + jump)

    #                 best_option = extrema(best_option, path, key = lambda x: x[0])

    #             #we iterated all of the available jumps, return the best
    #             return [best_option[0], jump_lock, best_option[2]]     

    #         else:
    #             #we dont have any available jumps
    #             #turn to the other player
    #             return self.minimax(board, -player, depth - 1)




    def heuristic(self, board: Checkers = None) -> int:
        if board:
            return board.get_score(player) - board.get_score(-player)
        else:
            return self.get_score(player) - self.get_score(-player)

