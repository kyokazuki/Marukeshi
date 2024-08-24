from classes.board import Board
from classes.bot import Bot
from classes.ratings import Ratings
import numpy as np
import copy, sys


def main():
    print("Marukeshi!")
    ROW = int(sys.argv[1])
    COL = int(sys.argv[2])
    MODE = int(sys.argv[3])

    current_board = Board(ROW, COL)
    bot = Bot(MODE)
    ratings = Ratings(ROW, COL)
    ratings.load()

    game_running = True

    while game_running == True:
        print('  a b c d ')
        for i, j in enumerate(current_board.array):
            print(f'{i+1}{j}')

        if current_board.erased == current_board.size:
            game_running = False
            print('Game over: Player wins!')
            break

        # human picking
        while True:
            inputs = [None, None]
            inputs[0] = input('Start point:')
            inputs[1] = input('End point:')
            try:
                if all([len(i)==2 for i in inputs]):
                    coords = []
                    for i in [0, 1]:
                        coords.append([int([*inputs[i]][0]) - 1, ord([*inputs[i]][1]) - 96 - 1])
                    if coords[0][0] == coords[1][0] or coords[0][1] == coords[1][1]:
                        if max(coords[0][0], coords[1][0]) <= ROW and max(coords[0][1], coords[1][1]) <= COL:
                            if sum(coords[0]) > sum(coords[1]):
                                coords.reverse()
                            if not np.any(current_board.array[coords[0][0]:coords[1][0]+1, coords[0][1]:coords[1][1]+1]):
                                human_pick = copy.deepcopy(current_board.array)
                                human_pick[coords[0][0]:coords[1][0]+1, coords[0][1]:coords[1][1]+1] = 1
                                break
                print('Invalid input!')
            except:
                print('Invalid input!')
        current_board.update(human_pick)

        print('  a b c d ')
        for i, j in enumerate(current_board.array):
            print(f'{i+1}{j}')

        if current_board.erased == current_board.size:
            game_running = False
            print('Game over: Computer wins!')
            break

        current_board.get_branches()
        next_board = bot.pick_move(current_board, ratings.dataframe)
        print("next_board:")
        print(next_board)
        current_board.update(next_board)

if __name__ == '__main__':
    main()

