from __future__ import annotations

import pygame

from typing import List, Tuple, NamedTuple, Callable

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

        self.difficulty = 5

        self.pc = Checkers.white
        self.player = Checkers.black



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

                            print(self.board)


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
                        print(self.board)


            
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
        origin, move = self.get_best_move(self.pc, self.alpha_beta, self.difficulty)
        print("pc moved:")
        print(origin, move)

        print(self.board.apply(origin, move))

        print(self.board)


    def turn(self, player: bool) -> None:
        if player:
            self.human_turn()
        else:
            self.pc_turn()


    # think of this function as the 0th level of the tree
    # it is just a minimax/alpha-beta iteration,
    # as the actual minimax/alpha-beta functions only return the heuristic
    # values of the nodes, this iteration will take care of also returning the best move/jump
    # NEGAMAX BABYYYYYYYYYY
    def get_best_move(self, player: int, algorithm: Callable, depth: int) -> (Checkers.Location, Checkers.Move):
        if self.board.won():
            return None

        # determine whether the player is allowed to move, or if he must jump
        player_moves: (Location, List[Jump]) = self.board.get_jumps(player = player, recursive = True)
        if not player_moves:
            player_moves: (Location, List[Move]) = self.board.get_moves(player = player)

        best_value = -inf
        best_option = None
        print(player_moves)
        for location, moves in player_moves:
            for move in moves:
                # generate the new board configuration
                new_board = copy.deepcopy(self.board)
                new_board.apply(location, move)

                path_value = -algorithm(new_board, -player, depth - 1)

                # check if the computed path is worth it
                if path_value >= best_value:
                    print("OKOKOKOKOK")
                    best_value = path_value
                    best_option = (location, move)

        # we iterated all of the available moves, return the best
        print(best_value, "###############")
        print(best_option)
        return best_option








    def negamax(self, board: Checkers, player: Checkers.Player, depth: int) -> int:
        winner = self.board.won()
        if winner:
            return inf if winner == player else -inf

        if depth == 0:
            return self.heuristic(player, board)

        # determine whether the player is allowed to move, or if he must jump
        player_moves: (Location, List[Jump]) = board.get_jumps(player = player)
        if not player_moves:
            player_moves: (Location, List[Move]) = board.get_moves(player = player)

        best_value = -inf
        for location, moves in player_moves:
            for move in moves:
                # generate the new board configuration
                new_board = copy.deepcopy(board)
                new_board.apply(location, move)

                best_value = max(best_value, -self.negamax(new_board, -player, depth - 1))

        # we iterated all of the available moves, return the best
        return best_value



    


    def alpha_beta(self, board: Checkers, player: Checkers.Player, depth: int, alpha: int = -inf, beta: int = inf) -> int:
        winner = self.board.won()
        if winner:
            return inf if winner == player else -inf

        if depth == 0:
            return self.heuristic(player, board)

        # prioritize moves that end in a promotion, requires some sorting of sort,
        # must check if sorting on every node is better than pruning (it should be for huge depths)
        player_moves: (Location, List[Jump]) = board.get_jumps(player = player, recursive = True)
        if not player_moves:
            player_moves: (Location, List[Move]) = board.get_moves(player = player)

        best_value = -inf
        for location, moves in player_moves:
            for move in moves:
                # generate the new board configuration
                new_board = copy.deepcopy(board)
                new_board.apply(location, move)

                best_value = max(best_value, -self.alpha_beta(new_board, -player, depth - 1, -beta, -alpha))
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    # cut-off
                    break

        # we iterated all of the available moves, return the best
        return best_value











    # negamax heuristic
    def heuristic(self, player: Player, board: Checkers = None) -> int:
        if not board:
            board = self.board

        return (board.get_count(player) - board.get_count(-player))*100 + (board.get_kings_count(player) - board.get_kings_count(-player))*50

