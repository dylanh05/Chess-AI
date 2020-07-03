import chess
import numpy as np
import random
from tensorflow import keras as ks


class Model:
    def __init__(self, color):
        self.color = color
        self.model = ks.models.load_model('./final')  # Change to model directory!
        print("Model loaded")

    def convert_board(self, board):

        bitboard = []
        for i in range(64):
            piece = str(board.piece_at(i))
            if piece == 'p':
                bitboard.append([-1, 0, 0, 0, 0, 0])
            if piece == 'r':
                bitboard.append([0, 0, 0, -1, 0, 0])
            if piece == 'n':
                bitboard.append([0, -1, 0, 0, 0, 0])
            if piece == 'b':
                bitboard.append([0, 0, -1, 0, 0, 0])
            if piece == 'q':
                bitboard.append([0, 0, 0, 0, -1, 0])
            if piece == 'k':
                bitboard.append([0, 0, 0, 0, 0, -1])
            if piece == 'P':
                bitboard.append([1, 0, 0, 0, 0, 0])
            if piece == 'R':
                bitboard.append([0, 0, 0, 1, 0, 0])
            if piece == 'N':
                bitboard.append([0, 1, 0, 0, 0, 0])
            if piece == 'B':
                bitboard.append([0, 0, 1, 0, 0, 0])
            if piece == 'Q':
                bitboard.append([0, 0, 0, 0, 1, 0])
            if piece == 'K':
                bitboard.append([0, 0, 0, 0, 0, 1])
            if piece == 'None':
                bitboard.append([0, 0, 0, 0, 0, 0])

        return bitboard

    def piece_score(self, board):

        score = 0
        for i in range(64):
            piece = str(board.piece_at(i))
            if piece == 'p':
                score -= 1
            if piece == 'r':
                score -= 4
            if piece == 'n':
                score -= 3
            if piece == 'b':
                score -= 3
            if piece == 'q':
                score -= 10
            if piece == 'k':
                score -= 20
            if piece == 'P':
                score += 1
            if piece == 'R':
                score += 4
            if piece == 'N':
                score += 3
            if piece == 'B':
                score += 3
            if piece == 'Q':
                score += 10
            if piece == 'K':
                score += 20

        return score

    def get_moves(self, board):

        moves = []
        for move in board.legal_moves:
            moves.append(move)
        return moves

    def eval_scores(self, board, moves):

        scores_numbs = []
        piece_scores = []
        positions = []

        for move in moves:
            board.push(chess.Move.from_uci(str(move)))
            positions.append(self.convert_board(board))
            piece_scores.append(self.piece_score(board))
            board.pop()
        scores = self.model.predict(np.array(positions))
        scores = scores.tolist()

        for score in scores:
            scores_numbs.append(score.index(max(score)))

        for i in range(len(scores_numbs)):
            scores_numbs[i] += piece_scores[i]
        return scores_numbs

    def pick_move(self, board):
        moves = self.get_moves(board)
        scores = self.eval_scores(board, moves)
        print(scores)
        # pick random in case of tie
        if self.color == "black":
            min_inds = [0]
            minimum = scores[0]
            for i in range(1, len(scores)):
                if scores[i] == minimum:
                    min_inds.append(int(i))
                if scores[i] < minimum:
                    min_inds = [int(i)]
                    minimum = scores[i]

            ind = random.randint(0, int(len(min_inds)) - 1)
            return moves[min_inds[ind]]

        if self.color == "white":
            max_inds = [0]
            maximum = scores[0]
            for i in range(1, len(scores)):
                if scores[i] == maximum:
                    max_inds.append(int(i))
                if scores[i] > maximum:
                    max_inds = [int(i)]
                    maximum = scores[i]

            ind = random.randint(0, int(len(max_inds)) - 1)

            return moves[max_inds[ind]]

    def make_move(self, board):
        move = self.pick_move(board)
        board.push(move)


    # For minimax implementation
    def eval_score(self, board, move):

        # Make the move on the board
        board.push(chess.Move.from_uci(str(move)))

        # Evaluate score of position
        position = self.convert_board(board)
        scores = self.model.predict(np.array([position]))
        piece_score = self.piece_score(board)

        # Undo the move
        board.pop()

        # Return score of the position that results from move
        scores = scores.tolist()
        score = scores[0].index(max(scores[0])) + piece_score

        return score
