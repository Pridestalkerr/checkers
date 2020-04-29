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

    # game = Game()

    # player = True
    # while game.on():
    # 	print(game)
    # 	game.turn(player)
    # 	player = not player

    # print(game)



    # pygame.init()

    # screen = pygame.display.set_mode((900, 900), 0, 32)

    # screen.fill((200, 200, 200))

    # img = pygame.image.load("white.png")
    # img = pygame.transform.scale(img, (100, 100))

    # img2 = pygame.image.load("black.png")
    # img2 = pygame.transform.scale(img2, (100, 100))

    # screen.blit(img, (100, 100))
    # screen.blit(img2, (300, 300))

    # mask = pygame.Surface((100, 100))
    # mask.fill((40, 122, 40))
    # inner = pygame.Surface((98, 98))
    # inner.fill((122, 40, 40))

    # mask.blit(inner, (1, 1))

    # screen.blit(mask, (100, 100))

    # rect = pygame.draw.rect(screen, (200, 200, 200), (0, 0, 100, 100))

    game = Game(background_color = (48, 25, 52), border_color = (120, 24, 74), black_cell_color = (48, 25, 52), white_cell_color = (120, 24, 74), border_size = 1)
    game.run()

    #print(game.board)



    
    #print(game.board.get_jump_sequences_for_pawn(Checkers.Location(1, 0)))


