from classes.board import Board
from classes.bot import Bot
from classes.ratings import Ratings
import numpy as np
import copy, sys


def main():
    print("Marukeshi!")
    ROW = int(sys.argv[1])
    COL = int(sys.argv[2])
    MODE0 = int(sys.argv[3])
    MODE1 = int(sys.argv[4])
    TOTAL_GAMES = int(sys.argv[5])

    bots = [Bot(MODE0), Bot(MODE1)]
    ratings = Ratings(ROW, COL)
    ratings.load()

    games_played = 0
    score = [0, 0]
    for _ in range(TOTAL_GAMES):
        current_board = Board(ROW, COL)
        game_running = True
        while game_running == True:
            for i in range(2):
                current_board.update_branches()
                next_board = bots[i].pick_move(current_board, ratings.dataframe)
                current_board.update(next_board)
                if current_board.erased == current_board.size:
                    score[1-i] += 1
                    game_running = False
                    print(f"score: {score}", end="\r", flush=True)
                    break

        games_played += 1
    print(f"score: {score}")

if __name__ == "__main__":
    main()

