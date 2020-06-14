import chess
import chess.pgn
import csv
import pandas as pd
import numpy as np

gamecount = 600

def board_to_bitboard(board):
    bitboard = []
    for i in range(64):
        if str(board.piece_at(i)) == 'p':
            bitboard.append(-1)
        if str(board.piece_at(i)) == 'r':
            bitboard.append(-4)
        if str(board.piece_at(i)) == 'n':
            bitboard.append(-2)
        if str(board.piece_at(i)) == 'b':
            bitboard.append(-3)
        if str(board.piece_at(i)) == 'q':
            bitboard.append(-10)
        if str(board.piece_at(i)) == 'k':
            bitboard.append(-5)
        if str(board.piece_at(i)) == 'P':
            bitboard.append(1)
        if str(board.piece_at(i)) == 'R':
            bitboard.append(4)
        if str(board.piece_at(i)) == 'N':
            bitboard.append(2)
        if str(board.piece_at(i)) == 'B':
            bitboard.append(3)
        if str(board.piece_at(i)) == 'Q':
            bitboard.append(10)
        if str(board.piece_at(i)) == 'K':
            bitboard.append(5)
        if str(board.piece_at(i)) == 'None':
            bitboard.append(0)
    return bitboard


#stockfish scores
def get_scores():
    with open('data/stockfish.csv', newline='') as rawdata:
        scores = []
        datareader = csv.reader(rawdata, delimiter=',')
        i = 0
        for row in datareader:
            gamescores = row[1]
            scores.extend(gamescores.split(" "))
            i += 1
            if i > gamecount:
                break

    dfscores = []
    for i in range(1, len(scores)):
        if scores[i] == 'NA' or scores[i] == '':
            scores[i] = 0
        if int(scores[i]) > 128:
            scores[i] = 128
        if int(scores[i]) < -128:
            scores[i] = -128
        dfscores.append([int(scores[i])])
    dfscores = dfscores[:len(dfscores)]
    return dfscores


def get_boards():
    boards = []
    pgn = open("data/data.pgn")
    for i in range(gamecount):
        game = chess.pgn.read_game(pgn)
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            boards.append(board_to_bitboard(board))
        if i % 100 == 0:
            print("Up to game no. " + str(i) + " saved")
    return boards

scores = np.asarray(get_scores())
positions = np.asarray(get_boards())
data = np.concatenate((positions, scores), axis=1)
df = pd.DataFrame(data)
export_csv = df.to_csv(r'C:\Users\daher\PycharmProjects\Chess\data\data.csv', index=None)


