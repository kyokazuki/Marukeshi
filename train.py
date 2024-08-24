from classes.board import Board, all_combinations, array_to_index
from classes.bot import Bot
from classes.ratings import Ratings
from copy import deepcopy
from time import time
from datetime import timedelta
import os, sys


def main():
    ROW = int(sys.argv[1])
    COL = int(sys.argv[2])
    if os.path.exists(f'{ROW}x{COL}') == False:
        print("Directory doesn't exist!")
        quit()
    size = ROW * COL
    sufficient_played_count = int(sys.argv[3])

    all_arrays = all_combinations(ROW, COL)
    starting_board = Board(ROW, COL)
    bots = [Bot(1), Bot(1)]
    ratings = Ratings(ROW, COL)
    ratings.load()

    start_time = time()
    for n in range(0, size):
        for array in all_arrays[n]:
            starting_board.update(array)
            print(starting_board.index)
            if ratings.dataframe[n].loc[starting_board.index, 1] >= sufficient_played_count:
                continue
            starting_board.get_branches()
            starting_board.get_equals()
            while ratings.dataframe[n].loc[starting_board.index, 1] < sufficient_played_count: 
                current_board = deepcopy(starting_board)
                game_running = True
                while game_running == True:
                    for i in range(2):
                        bots[i].update_history(current_board.equals)
                        current_board.update(bots[i].pick_move(current_board, ratings.dataframe))
                        if current_board.erased == size:
                            game_running = False
                            winner = 1 - i
                            break
                        current_board.get_branches()
                        current_board.get_equals()
                ratings.update(bots, winner)
                for i in range(2):
                    bots[i].clear_history()
        ratings.write()

    print(f'session time: {timedelta(seconds = round(time() - start_time))}')


if __name__ == "__main__":
    main()

