import pygame
import math
from pygame.locals import *
from ai import *
from minimax import *

use_minimax = False

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def draw_board(board):
    for i in range(64):
        x = (i % 8)*75
        y = math.floor((63 - i)/8)*75
        piece = str(board.piece_at(i))
        if piece == 'p':
            piece = Sprite('./assets/bp.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'b':
            piece = Sprite('./assets/bb.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'n':
            piece = Sprite('./assets/bkn.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'r':
            piece = Sprite('./assets/br.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'k':
            piece = Sprite('./assets/bk.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'q':
            piece = Sprite('./assets/bq.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'P':
            piece = Sprite('./assets/wp.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'B':
            piece = Sprite('./assets/wb.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'N':
            piece = Sprite('./assets/wkn.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'R':
            piece = Sprite('./assets/wr.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'K':
            piece = Sprite('./assets/wk.png', [x, y])
            screen.blit(piece.image, piece.rect)
        if piece == 'Q':
            piece = Sprite('./assets/wq.png', [x, y])
            screen.blit(piece.image, piece.rect)


def get_square(pos):
    x = pos[0]
    y = pos[1]
    for i in range(8):
        if i*75 <= x < i*75+75:
            col = i
    for i in range(8):
        if i*75 < y < i*75+75:
            row = 8-i

    if col == 0:
        col = 'a'
    if col == 1:
        col = 'b'
    if col == 2:
        col = 'c'
    if col == 3:
        col = 'd'
    if col == 4:
        col = 'e'
    if col == 5:
        col = 'f'
    if col == 6:
        col = 'g'
    if col == 7:
        col = 'h'

    square = str(col)+str(row)

    return square


gerald = Model("black")
board = chess.Board()
BackGround = Background('./assets/board.gif', [0, 0])

pygame.init()
screen = pygame.display.set_mode((600, 600))
running = 1


# move = True is white's turn to move, move = False is black's turn to move
move = True
# move_next signals white is awaiting a second square for the move
move_next = False
# next_move is the "uci" string for whites move
next_move = ''


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == MOUSEBUTTONDOWN:

            if move_next:
                pos = get_square(pygame.mouse.get_pos())
                if pos != next_move:
                    move = chess.Move.from_uci(next_move+pos)
                    if move in board.legal_moves:
                        board.push(move)
                        if use_minimax:
                            minimax = Minimax(1, gerald)
                            minimax.run(board)
                        else:
                            gerald.make_move(board)
                        move = True
                        move_next = False
                        break
                    else:
                        next_move = ''
                        move = True
                        move_next = False
                        break
                else:
                    move = True
                    move_next = False
                    next_move = ''
                    break

            if move:
                next_move = get_square(pygame.mouse.get_pos())
                move = False
                move_next = True

    if board.is_game_over():
        if move:
            print("White wins")
        if not move:
            print("Black wins")
        break

    screen.fill((0, 0, 0))
    screen.blit(BackGround.image, BackGround.rect)
    draw_board(board)
    pygame.display.flip()

pygame.quit()
