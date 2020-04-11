from game import *



if __name__ == "__main__":

    # board = Checkers([
    #     # a    b    c    d    e    f    g    h
    #     [0, -1, 0, -1, 0, -1, 0, -1],   #0
    #     [-1, 0, -1, 0, -1, 0, -1, 0],   #1
    #     [0, -1, 0, -1, 0, -1, 0, -1],   #2
    #     [0, 0, 0, 0, 0, 0, 0, 0],   #3
    #     [0, 0, 0, 0, 0, 0, 0, 0],   #4
    #     [1, 0, 1, 0, 1, 0, 1, 0],   #5
    #     [0, 1, 0, 1, 0, 1, 0, 1],   #6
    #     [1, 0, 1, 0, 1, 0, 1, 0]    #7
    # ])

    # print(board)

    # print(board.move(Pair(5, 0), Pair(-1, 1)))
    # print(board.move(Pair(4, 1), Pair(-1, 1)))
    # print(board.get_valid_jumps(Pair(2, 1)))
    # print(board)

    # print("looks ok...")

    # print(board.get_all_white_jumps())

    game = Game()

    player = True
    while game.on():
    	print(game)
    	game.turn(player)
    	player = not player

    print(game)