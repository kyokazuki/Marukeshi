from .board import all_combinations, array_to_index
import os
import numpy as np
import pandas as pd


class Ratings:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.size = self.row * self.col
        self.dataframe = []

    def create(self):
        print("Initializing combinations...", end="", flush=True)
        all_arrays = all_combinations(self.row, self.col)
        print("done")
        print("Resetting ratings...", end="", flush=True)
        for n in range(0, self.size + 1):
            index = []
            for array in all_arrays[n]:
                index.append(array_to_index(array))
            numbers = np.full((len(index), 1), 0)
            rating = np.full((len(index), 1), 0.5)
            data = np.column_stack((numbers, rating))
            self.dataframe.append(pd.DataFrame(data = data, index = index))
            self.dataframe[n] = self.dataframe[n].astype({0: int, 1: float})
        print("done")

    def load(self):
        for n in range(0, self.size + 1):
            self.dataframe.append(pd.read_csv(
                f'{self.row}x{self.col}/board-{n}',
                delimiter = ' ',
                dtype = {0: 'str'},
                header = None,
                index_col = 0
            ))

    def update(self, bots, winner):
        for i in bots[winner].history:
            n = i.count('1')
            self.dataframe[n].loc[i, 1] += 1
            self.dataframe[n].loc[i, 2] = round((self.dataframe[n].loc[i, 2]+1)/2, 3)
        for i in bots[1 - winner].history:
            n = i.count('1')
            self.dataframe[n].loc[i, 1] += 1
            self.dataframe[n].loc[i, 2] = round(self.dataframe[n].loc[i, 2]/2, 3)

    def write(self):
        print("Writing...", end="", flush=True)
        for n in range(0, self.row * self.col + 1):
            self.dataframe[n].to_csv(
                f'{self.row}x{self.col}/board-{n}',
                sep = ' ',
                header = False
            )
        print("done")

