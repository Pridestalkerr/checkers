import pygame



class GameUI:

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


        # ----
        # ---- SAVING SIZES
        # ----

        self.display_width = display_width
        self.display_height = display_height

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.board_width = cell_width * 8
        self.board_height = cell_height * 8

        self.border_size = border_size


        # ----
        # ---- SAVING COLORS
        # ----

        self.background_color = background_color
        self.border_color = border_color
        self.black_cell_color = black_cell_color
        self.white_cell_color = white_cell_color
        self.font_color = font_color


        # ----
        # ---- SAVING SPRITES
        # ----

        self.black_pawn = pygame.transform.scale(pygame.image.load(black_sprite), (cell_width, cell_height))
        self.black_king = pygame.transform.scale(pygame.image.load(black_king_sprite), (cell_width, cell_height))
        self.white_pawn = pygame.transform.scale(pygame.image.load(white_sprite), (cell_width, cell_height))
        self.white_king = pygame.transform.scale(pygame.image.load(white_king_sprite), (cell_width, cell_height))


        # ----
        # ---- INIT
        # ----

        # generating cell surfaces
        self.black_cell = pygame.Surface((cell_width, cell_height))
        self.black_cell.fill(black_cell_color)
        self.white_cell = pygame.Surface((cell_width, cell_height))
        self.white_cell.fill(white_cell_color)

        # generating board surface
        self.board = pygame.Surface((self.board_width, self.board_height))
        self.board_rect = self.board.get_rect(center = pygame.Rect(0, 0, 900, 900).center)
        self.draw_cells_on(self.board)

        # border mask
        self.border = pygame.Surface((self.board_width + 2*border_size, self.board_height + 2*border_size))
        self.border.fill(border_color)
        self.border_rect = self.border.get_rect(center = pygame.Rect(0, 0, 900, 900).center)

        # window init
        self.caption = caption
        self.logo = pygame.transform.scale(pygame.image.load(logo), (32, 32))
        if auto_init:
            self.init_window()









    def init_window(self) -> None:
        pygame.display.set_icon(self.logo)
        pygame.font.init()
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()


    def draw_background(self) -> None:
        self.display.fill(self.background_color)


    def draw_border(self) -> None:
        if self.border_size == 0:
            return
        
        self.display.blit(self.border, self.border_rect)


    # static
    def draw_cells_on(self, board: "pygame.Surface") -> None:
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    board.blit(self.white_cell, (self.mapIndexToCoord(i, j)))
                else:
                    board.blit(self.black_cell, (self.mapIndexToCoord(i, j)))


    def draw_pawns_on(self, config: "Checkers", board: "pygame.Surface") -> None:
        for i in range(8):
            for j in range(8):
                if config.is_black(config.board[i][j]):
                    if config.is_king(config.board[i][j]):
                        board.blit(self.black_king, (self.mapIndexToCoord(i, j)))
                    else:
                        board.blit(self.black_pawn, (self.mapIndexToCoord(i, j)))
                elif config.is_white(config.board[i][j]):
                    if config.is_king(config.board[i][j]):
                        board.blit(self.white_king, (self.mapIndexToCoord(i, j)))
                    else:
                        board.blit(self.white_pawn, (self.mapIndexToCoord(i, j)))


    def draw_board(self) -> None:
        self.display.blit(self.board, self.board_rect)

    def draw_winner(self, winner: str) -> None:
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text = font.render(winner + "wins", True, self.white_cell_color)

        text_rect = text.get_rect()


        self.display.blit(text, ((self.display_width - text_rect.width)/ 2, 0))



    def draw(self, config: "Checkers") -> None:
        self.draw_background()
        self.draw_border()
        self.draw_cells_on(self.board)
        self.draw_pawns_on(config, self.board)
        self.draw_board()


    def mapIndexToCoord(self, row: int, col: int) -> (int, int):
        return self.cell_width * col, self.cell_height * row


    def mapCoordToIndex(self, x: int, y: int) -> (int, int):
        y -= 50
        x -= 50
        return int(y / self.cell_height), int(x / self.cell_width)


    #should be overloaded
    def render(self) -> None:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()


    def update(self) -> None:
        pygame.display.update()
        