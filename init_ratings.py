from classes.ratings import Ratings
import os, shutil, sys


def main():
    ROW = int(sys.argv[1])
    COL = int(sys.argv[2])
    if os.path.exists(f"{ROW}x{COL}") == True:
        if input("Directory exists! Reset? (y/N): ") == "y":
            shutil.rmtree(f'{ROW}x{COL}')
        else:
            quit()
    os.makedirs(f"./{ROW}x{COL}")
    ratings = Ratings(ROW, COL)
    ratings.create()
    ratings.write()


if __name__ == "__main__":
    main()

