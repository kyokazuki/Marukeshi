from .board import Board, array_to_index, erased, erasable
import random as rnd
import numpy as np


def lowest_rating(row, col, branches, dataframe):
    worst_branch = None
    lowest_rating = 1
    for b1 in branches:
        rating = dataframe[erased(b1)][2][array_to_index(b1)]
        if rating == 0:
            return [b1, rating]
        if rating <= lowest_rating:
            worst_branch = b1
            lowest_rating = rating
    return [worst_branch, lowest_rating]

def highest_lowest_rating(row, col, branches, dataframe):
    best_branch = None
    highest_rating = 0
    for b1 in branches:
        b2 = branches(row, col, b1, erasable(row, col, b1)) 
        b2_lowest_rating = lowest_rating(row, col, b2, dataframe)[1]
        if b2_lowest_rating >= highest_rating:
            best_branch = b1
            highest_rating = b2_lowest_rating
    return [best_branch, highest_rating]

def lowest_highest_lowest_rating(row, col, branches, dataframe):
    worst_branch = None
    lowest_rating = 0
    for b1 in branches:
        b2 = branches(row, col, b1, erasable(row, col, b1)) 
        b2_highest_lowest_rating = highest_lowest_rating(row, col, b2, dataframe)[1]
        if b2_highest_lowest_rating == 1:
            return [b1, b2_highest_lowest_rating]
        if b2_highest_lowest_rating >= lowest_rating:
            worst_branch = b1
            lowest_rating = b2_lowest_rating
    return [worst_branch, lowest_rating]


class Bot:
    def __init__(self, mode):
        self.mode = mode
        self.history = []

    def update_history(self, equals):
        self.history += equals
    
    def clear_history(self):
        self.history = []

    def pick_move(self, board, dataframe):
        # random board
        if self.mode == 1:
            choice = rnd.choice(board.branches) 
            return choice
        
        # random board with weight of 1-rating
        # if self.mode == 2:
        #     if current_board.erased == current_board.board_size - 1:
        #         return current_board.all_combinations[current_board.board_size][0]
        #     else:
        #         weights = []
        #         for b in current_board.branches:
        #             weights.append(1-dataframe[current_board.erased(b)][2][array_to_index(b)])
        #         if sum(weights) == 0:
        #             return rnd.choice(current_board.branches)
        #         else:
        #             return rnd.choices(current_board.branches, weights = weights, k=1)[0]

        # lowest rating for opponent
        if self.mode == 2:
            return lowest_rating(board.row, board.col, board.branches, dataframe)[0]
        
        # highest rating for next self turn (assuming opponent pick lowest rating for self)
        if self.mode == 3:
            return highest_lowest_rating(board.row, board.col, board.branches, dataframe)[0]
        
        # 2 steps ahead with lowest rating
        if self.mode == 4:
            return lowest_highest_lowest_rating(board.row, board.col, board.branches, dataframe)[0]

