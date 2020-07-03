import numpy as np
import chess


class Node:
    def __init__(self, parent, val):
        self.parent = parent
        self.val = val
        self.children = []
        self.score = 0


class Tree:
    def __init__(self, n, parent_moves, model, board):
        self.n = n
        self.layers = [[] for x in range(n+1)]
        self.layers_scores = [[] for x in range(n+1)]
        self.model = model

        # Create move tree with all possible moves looking n turns ahead
        for move in parent_moves:
            self.layers[0].append(Node("None", move))

        for i in range(1, n+1):
            for move in self.layers[i-1]:
                board.push(move.val)
                for response in self.model.get_moves(board):
                    self.layers[i].append(Node(move, response))
                    move.children.append(self.layers[i][-1])
                board.pop()

    def print_tree(self):
        for i in range(len(self.layers)):
            layer = self.layers[i]
            print("Layer " + str(i) + " is of length: " + str(len(layer)))
            for j in range(len(layer)):
                move = layer[j]
                print("Move: " + str(move.val) + ", Parent: " + str(move.parent) + ", Score: " + str(move.score))

    # For minimax implementation
    def eval_tree(self, board):
        # Evaluate score of board after traversing the tree from parent
        for i in range(len(self.layers)):

            # For first layer, no parent moves to consider
            # For second layer, we must first push the move from the parent node before evaluating score, and so on
            for move in self.layers[i]:
                if i == 1:
                    board.push(move.parent.val)
                if i == 2:
                    board.push(move.parent.parent.val)
                    board.push(move.parent.val)
                self.layers_scores[i].append(self.model.eval_score(board, move.val))
                if i == 1:
                    board.pop()
                if i == 2:
                    board.pop()
                    board.pop()

