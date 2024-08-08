from classes.board import Board, all_combinations, array_to_index
from classes.player import Player
from classes.ratings import Ratings
import config
from copy import deepcopy
from time import time
from datetime import timedelta
import os, sys


def main():
    row = int(sys.argv[1])
    col = int(sys.argv[2])
    if os.path.exists(f'{row}x{col}') == False:
        print("Directory doesn't exist!")
        quit()
    size = row * col
    sufficient_played_count = int(sys.argv[3])

    all_arrays = all_combinations(row, col)
    starting_board = Board(row, col)
    players = [Player(1), Player(1)]
    ratings = Ratings(row, col)
    ratings.load()

    start_time = time()
    for n in range(0, size):
        for array in all_arrays[n]:
            starting_board.update(array)
            print(starting_board.index)
            needed_played_count = sufficient_played_count - ratings.dataframe[n].loc[starting_board.index, 1] 
            if needed_played_count <= 0:
                continue
            starting_board.get_branches()
            starting_board.get_equals()
            for _ in range(needed_played_count):
                current_board = deepcopy(starting_board)
                game_running = True
                while game_running == True:
                    for i in range(2):
                        players[i].update_history(current_board.equals)
                        current_board.update(players[i].pick_move(current_board.branches, ratings.dataframe))
                        if current_board.erased == size:
                            game_running = False
                            winner = 1 - i
                            break
                        current_board.get_branches()
                        current_board.get_equals()
                ratings.update(players, winner)
                for i in range(2):
                    players[i].clear_history()
        ratings.write()

    print(f'session time: {timedelta(seconds = round(time() - start_time))}')


if __name__ == "__main__":
    main()

