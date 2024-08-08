import itertools as it
from copy import deepcopy
import numpy as np


def all_combinations(row, col):
    all_combinations = []
    board_coordinates = list(it.product(range(row), range(col)))
    for n in range(0, row * col + 1):
        all_combinations.append([])
        for coordinates in list(it.combinations(board_coordinates, n)):
            b = np.zeros((row, col), dtype=int)
            for (r, c) in coordinates:
                b[r, c] = 1
            all_combinations[n].append(b)
    return all_combinations


def array_to_index(array):
    index = ''
    for r in array:
        for c in r:
            index += str(c)
    return index


def erased(array):
    return np.count_nonzero(array)

# longest length of consecutive 0's in an array
def erasable(row, col, array):
    erasable = 0
    for r in range(row):
        for k, g in it.groupby(array[r,:]):
            l = len(list(g))
            if k == 0 and l == row:
                return row
            if k == 0 and l > erasable:
                erasable = l
    for c in range(col):
        for k, g in it.groupby(array[:,c]):
            l = len(list(g))
            if k == 0 and l == col:
                return col
            if k == 0 and l > erasable:
                erasable = l
    return erasable


# returns valid boards([arr])
def branches(row, col, array, erasable):
    branches = []
    for r in range(0, row):
        for c in range(0, col):
            if array[r,c] == 0:
                branch = deepcopy(array)
                branch[r,c] = 1
                branches.append(deepcopy(branch))
                for n in range(1, min(erasable, col-c)):
                    if np.all(array[r, c:c+n+1]==0):
                        branch = deepcopy(array)
                        branch[r, c:c+n+1] = 1
                        branches.append(deepcopy(branch))
                    else:
                        break
                for n in range(1, min(erasable, row-r)):
                    if np.all(array[r:r+n+1, c]==0):
                        branch = deepcopy(array)
                        branch[r:r+n+1, c] = 1
                        branches.append(deepcopy(branch))
                    else:
                        break
    return branches


def equals(row, col, size, array, index, erased):
    equals = []
    if erased == 0 or erased == size:
        return [index]

    elif erased == size - 1:
        array = deepcopy(array)
        for i in range(0, 4):
            equals.append(array_to_index(np.rot90(array, k = i)))
        return equals

    elif erased >= 1 and erased < min(row, col):
        array = deepcopy(array)
        # rotate and flip-rotate
        for i in range(0, 4):
            equals.append(np.rot90(array, k = i))
            equals.append(np.rot90(np.flipud(array), k = i))
        # remove duplicates and convert to index
        equals_unique = []
        for b in equals:
            i = array_to_index(b)
            if i not in equals_unique:
                equals_unique.append(i)
        return equals_unique
        
    else:
        # parallels
        parallels = []
        stripped = deepcopy(array)
        while True:
            if np.all(stripped, axis = 0)[0]: 
                stripped = stripped[0:stripped.shape[0], 1:stripped.shape[1]]
            else:
                break
        while True:
            if np.all(stripped, axis = 0)[-1]: 
                stripped = stripped[0:stripped.shape[0], 0:stripped.shape[1]-1]
            else:
                break
        while True:
            if np.all(stripped, axis = 1)[0]: 
                stripped = stripped[1:stripped.shape[0], 0:stripped.shape[1]]
            else:
                break
        while True:
            if np.all(stripped, axis = 1)[-1]: 
                stripped = stripped[0:stripped.shape[0]-1, 0:stripped.shape[1]]
            else:
                break
        for r in range(0, row - stripped.shape[0] + 1):
            for c in range(0, col - stripped.shape[1] + 1):
                b = np.ones((row, col), dtype=int)
                b[r:r+stripped.shape[0], c:c+stripped.shape[1]] = stripped
                parallels.append(b)

        # rotate and flip-rotate
        equals = []
        for b in parallels:
            for i in range(0, 4):
                equals.append(np.rot90(b, k = i))
                equals.append(np.rot90(np.flipud(b), k = i))
    
        # convert to index and remove identicals
        equals_unique = []
        for b in equals:
            i = array_to_index(b)
            if i not in equals_unique:
                equals_unique.append(i)
        
        return equals_unique


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.size = self.row * self.col

        self.array = np.zeros((self.row, self.col), dtype=int)
        self.index = '0' * self.size
        self.erased = 0
        self.erasable = max(self.row, self.col)

        self.branches = None
        self.equals = None

    def update(self, array):
        self.array = array
        self.index = array_to_index(self.array)
        self.erased = erased(self.array) 
        self.erasable = erasable(self.row, self.col, self.array)

    def get_branches(self):
        self.branches = branches(self.row, self.col, self.array, self.erasable)

    # returns equal boards([str])
    def get_equals(self):
        self.equals = equals(self.row, self.col, self.size, self.array, self.index, self.erased)

