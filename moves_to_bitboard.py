
def move_to_bitboard(game):

    board = chess.Board()

    # prepares move list
    moves = game
    moves = moves.split(' ')
    i = 0

    while (i < len(moves)):
        del moves[i]
        i = i + 2

    for i in range(0, len(moves)):
        global count
        bitboard = []
        move = moves[i]
        board.push_san(move)
        for j in range(0, 64):
            piece = str(board.piece_at(j))
            if(piece == 'P'):
                piece = 1
            if(piece == 'p'):
                piece = -1
            if(piece == 'R'):
                piece = 5
            if(piece == 'r'):
                piece = -5
            if(piece == 'B'):
                piece = 3
            if(piece == 'b'):
                piece = -3
            if(piece == 'Q'):
                piece = 9
            if(piece == 'q'):
                piece = -9
            if(piece == 'K'):
                piece = 10
            if(piece == 'k'):
                piece = -10
            if(piece == 'None'):
                piece = 0
            if(piece == 'N'):
                piece = 2
            if(piece == 'n'):
                piece = -2
            bitboard.append(piece)
        #stores every bitboard
        data.append(bitboard)
