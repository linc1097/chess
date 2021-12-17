import pygame
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
from move import Move
from player import Player, HumanPlayer

class Game:

	board = [[None]*8 for _ in range(8)]

	def move(self, move):
		if move.en_passant:
			if move.piece.color == C.WHITE:
				pass
			else:
				pass
		else:
			move.piece.move(move)
			self.board[move.x][move.y] = move.piece

	def game_over(self):
		return False

	def play(self):
		white_king, black_king = game2.setup_game()
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')


		dragging = False
		moving_piece = None
		running = True
		x = 0
		y = 0
		white = HumanPlayer(color = C.WHITE, king = white_king)
		black = HumanPlayer(color = C.BLACK, king = black_king)
		while running:
			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			move = white.make_move(screen, self.board)
			self.move(move)

			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			if self.game_over():
				break

			move = black.make_move(screen, self.board)
			self.move(move)

			if self.game_over():
				break

	def setup_game(self):
		white_king = pygame.image.load('images/white_king.png')
		white_king = pygame.transform.scale(white_king, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_queen = pygame.image.load('images/white_queen.png')
		white_queen = pygame.transform.scale(white_queen, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_rook = pygame.image.load('images/white_rook.png')
		white_rook = pygame.transform.scale(white_rook, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_knight = pygame.image.load('images/white_knight.png')
		white_knight = pygame.transform.scale(white_knight, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_bishop = pygame.image.load('images/white_bishop.png')
		white_bishop = pygame.transform.scale(white_bishop, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_pawn = pygame.image.load('images/white_pawn.png')
		white_pawn = pygame.transform.scale(white_pawn, (C.SQUARE_SIZE, C.SQUARE_SIZE))

		black_king = pygame.image.load('images/black_king.png')
		black_king = pygame.transform.scale(black_king, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_queen = pygame.image.load('images/black_queen.png')
		black_queen = pygame.transform.scale(black_queen, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_rook = pygame.image.load('images/black_rook.png')
		black_rook = pygame.transform.scale(black_rook, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_knight = pygame.image.load('images/black_knight.png')
		black_knight = pygame.transform.scale(black_knight, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_bishop = pygame.image.load('images/black_bishop.png')
		black_bishop = pygame.transform.scale(black_bishop, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_pawn = pygame.image.load('images/black_pawn.png')
		black_pawn = pygame.transform.scale(black_pawn, (C.SQUARE_SIZE, C.SQUARE_SIZE))

		pieces = []
		for i in range(8):
			pieces.append(Piece(C.BLACK, C.PAWN, black_pawn, i, 1))
			pieces.append(Piece(C.WHITE, C.PAWN, white_pawn, i, 6))

		pieces.append(Piece(C.BLACK, C.ROOK, black_rook, 0, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, black_knight, 1, 0))
		pieces.append(Piece(C.BLACK, C.BISHOP, black_bishop, 2, 0))
		pieces.append(Piece(C.BLACK, C.QUEEN, black_queen, 3, 0))
		black_king_piece = Piece(C.BLACK, C.KING, black_king, 4, 0)
		pieces.append(black_king_piece)
		pieces.append(Piece(C.BLACK, C.BISHOP, black_bishop, 5, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, black_knight, 6, 0))
		pieces.append(Piece(C.BLACK, C.ROOK, black_rook, 7, 0))

		pieces.append(Piece(C.WHITE, C.ROOK, white_rook, 0, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, white_knight, 1, 7))
		pieces.append(Piece(C.WHITE, C.BISHOP, white_bishop, 2, 7))
		pieces.append(Piece(C.WHITE, C.QUEEN, white_queen, 3, 7))
		white_king_piece = Piece(C.WHITE, C.KING, white_king, 4, 7)
		pieces.append(white_king_piece)
		pieces.append(Piece(C.WHITE, C.BISHOP, white_bishop, 5, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, white_knight, 6, 7))
		pieces.append(Piece(C.WHITE, C.ROOK, white_rook, 7, 7))

		for piece in pieces:
			self.board[piece.x][piece.y] = piece
		return (white_king_piece, black_king_piece)
	
	def print_board(self):
		for row in self.board[::-1]:
			print(row)




game2 = Game()
game2.play()


