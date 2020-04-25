from checkers import *
from math import inf




class GameCLI:

    def __init__(self) -> None:

        self.board = Checkers()





    def __repr__(self) -> str:
        return str(self.board)


    def draw() -> None:
        print(self)






    def prompt_jump(self) -> None:
        jump = self.parse_input(input("Jump: "))


    def prompt_move(self) -> None:
        move = self.parse_input(input("Move: "))

        

        


    



    def parse_input(self, attempt: str) -> Tuple[Pair, Pair]:
        #5a 4b
        attempt = attempt.split(' ')
        origin = Pair(int(attempt[0][0]), ord(attempt[0][1]) - 97)
        move = Pair(int(attempt[1][0]) - origin.row, ord(attempt[1][1]) - 97 - origin.col)

        return (origin, move)



    