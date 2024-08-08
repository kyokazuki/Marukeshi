import config, board, data, player, game
from board import Board
from player import Player
from game import Game
import time
from datetime import timedelta

# session start
session_start = time.time()
player0_df = data.load(config.board_row, config.board_col, config.player0_data_strat)
player1_df = data.load(config.board_row, config.board_col, config.player1_data_strat)
player_score = [0, 0]


for i in range(0, config.games_total):
    game = Game(board.board_list[0][0], [config.player0_strat, config.player1_strat], config.match_first_move)
    game.run([player0_df, player1_df])
    player_score[game.current_player] += 1
    print(f'{i+1}: player{game.current_player} wins!')

# session end
print(f'games played: {config.games_total}')
print(f'player score: {player_score}')
print(f'session time: {timedelta(seconds = round(time.time() - session_start))}')