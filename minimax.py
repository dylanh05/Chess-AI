from ai import *
from tree import *

class Minimax:

    def __init__(self, n, ai):
        self.n = n
        self.ai = ai

    def pick_move(self, tree):
        # turn = True is white
        turn = bool(tree.n % 2)

        first_layer = True
        for i in range(len(tree.layers)-1):
            ind = tree.n-i-1
            j = 0
            for node in tree.layers[ind]:
                if first_layer:
                    mini = tree.layers_scores[ind+1][j]
                    maxi = tree.layers_scores[ind+1][j]
                    for move in node.children:
                        if not turn:
                            if tree.layers_scores[ind+1][j] < mini:
                                mini = tree.layers_scores[ind+1][j]
                        else:
                            if tree.layers_scores[ind+1][j] > maxi:
                                maxi = tree.layers_scores[ind+1][j]
                        j += 1
                    if not turn:
                        node.score = mini
                    else:
                        node.score = maxi

                else:
                    mini = 1000
                    maxi = -1000
                    for move in node.children:
                        if not turn:
                            if move.score < mini:
                                mini = move.score
                        else:
                            if move.score > maxi:
                                maxi = move.score
                    if not turn:
                        node.score = mini
                    else:
                        node.score = maxi

            first_layer = False
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

