from classes.board import Board
from classes.player import Player
from classes.ratings import Ratings
import numpy as np
import copy


def main():
    while True:
        print("Marukeshi!")
        ROW = 4
        COL = 4
        try:
            mode = int(input("Select mode:(1,2,3,4,5)"))
        except:
            print("Invalid input!")

        current_board = Board(ROW, COL)
        players = [Player(0), Player(mode)]
        ratings = Ratings(ROW, COL, mode)
        ratings.load()

        game_running = True
        first_move = players[0]

        while game_running == True:
            print('  a b c d ')
            for i, j in enumerate(current_board.array):
                print(f'{i+1}{j}')

            if current_board.erased == current_board.size:
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
                print('Game over!')
                break

            next_board = players[1].pick_move(current_board, ratings.dataframe)
            print("next_board:")
            print(next_board)
            current_board.update(next_board)

if __name__ == '__main__':
    main()

