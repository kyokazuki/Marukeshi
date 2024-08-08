from classes.ratings import Ratings
import os, shutil, sys


def main():
    row = int(sys.argv[1])
    col = int(sys.argv[2])
    if os.path.exists(f'{row}x{col}') == True:
        if input("Directory exists! Reset? (y/N): ") == 'y':
            shutil.rmtree(f'{row}x{col}')
        else:
            quit()
    os.makedirs(f'./{row}x{col}')
    ratings = Ratings(row, col)
    ratings.create()
    ratings.write()


if __name__ == '__main__':
    main()

