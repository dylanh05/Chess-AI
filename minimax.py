from ai import *
from tree import *


class Minimax:

    def __init__(self, n, ai):
        self.n = n
        self.ai = ai

    def pick_move(self, tree):
        # turn = True is white
        turn = bool(tree.n % 2)

        for i in range(len(tree.layers)-1):
            ind = tree.n-i-1
            for move in tree.layers[ind]:
                if len(move.children) != 0:
                    minormax = move.children[0].score
                    # Find min or max score, update parents score
                    for j in range(len(move.children)):
                        child = move.children[j]
                        if turn:
                            if child.score > minormax:
                                minormax = child.score
                        else:
                            if child.score < minormax:
                                minormax = child.score
                    move.score = minormax
                else:
                    move.score = 0
            turn = not turn

        mini = tree.layers[0][0].score
        mini_ind = 0
        for i in range(len(tree.layers[0])):
            if tree.layers[0][i].score < mini:
                mini = tree.layers[0][i].score
                mini_ind = i

        return tree.layers[0][mini_ind].val


    def run(self, board):
        move_tree = Tree(self.n, self.ai.get_moves(board), self.ai, board)
        move_tree.eval_tree(board)
        board.push(self.pick_move(move_tree))
        move_tree.print_tree()

