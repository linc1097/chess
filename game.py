import pygame
import time
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
from move import Move
from player import Player, HumanPlayer, RandomPlayer, MiniMaxPlayer

class Game:

	board = [None] * 64
	progress_num = 0

	def move(self, move):
		if move.en_passant:
			if move.piece.color == C.WHITE:
				self.board[move.position+8] = None
			else:
				self.board[move.position-8] = None

		if move.castle:
			if move.castle == C.KINGS_SIDE:
				self.board[move.position-1] = self.board[move.position+1]
				self.board[move.position-1].position = move.position-1
				self.board[move.position+1] = None
			else:
				self.board[move.position+1] = self.board[move.position-2]
				self.board[move.position+1].position = move.position+1
				self.board[move.position-2] = None

		if move.promote:
			move.piece.promote(move.promote)

		self.board[move.piece.position] = None
		self.board[move.position] = move.piece
		return move.piece.move(move)

	#given king of player whose turn it is
	def game_over(self, king, positions, made_progress):
		legal_moves = Utils.all_legal_moves(self.board, king.color)
		#print("legal_moves: " + str(legal_moves))
		if not legal_moves:
			if Utils.is_attacked(self.board, king):
				return C.BLACK_WIN if king.color == C.WHITE else C.WHITE_WIN
			else:
				return C.DRAW
		
		position = str(self.board)
		if position in positions.keys():
			positions[position] += 1
			if positions[position] == 3:
				return C.DRAW
		else:
			positions[position] = 1

		if not made_progress[0] and not made_progress[1]:
			self.progress_num += 1
		else:
			self.progress_num = 0

		if self.progress_num == 100:
			return C.DRAW

	def makes_progress(self, move):
		return self.board[move.position] or move.piece.kind == C.PAWN
					
	def play(self):
		white_king, black_king = game2.setup_game()
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')
		positions = {}


		dragging = False
		moving_piece = None
		running = True
		white = HumanPlayer(color = C.WHITE, king = white_king, other_king = black_king)
		black = MiniMaxPlayer(color = C.BLACK, king = black_king, other_king = white_king)
		en_passant = None
		made_progress = [False, False]
		while running:
			pygame.event.get()
			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			game_result = self.game_over(white_king, positions, made_progress)
			if game_result:
				print(C.RESULT[game_result])
				break

			move = white.make_move(self.board, screen = screen)
			made_progress[0] = self.makes_progress(move)
			if en_passant:
				en_passant.en_passant = False
			en_passant = self.move(move)

			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			game_result = self.game_over(black_king, positions, made_progress)
			if game_result:
				print(C.RESULT[game_result])
				break

			move = black.make_move(self.board, screen = screen)
			made_progress[1] = self.makes_progress(move)


			if en_passant:
				en_passant.en_passant = False
			en_passant = self.move(move)


	def setup_game(self):
		pieces = []
		for i in range(8):
			pieces.append(Piece(C.BLACK, C.PAWN, C.black_pawn, 8+i))
			pieces.append(Piece(C.WHITE, C.PAWN, C.white_pawn, 48+i))

		pieces.append(Piece(C.BLACK, C.ROOK, C.black_rook, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, C.black_knight, 1))
		pieces.append(Piece(C.BLACK, C.BISHOP, C.black_bishop, 2))
		pieces.append(Piece(C.BLACK, C.QUEEN, C.black_queen, 3))
		black_king_piece = Piece(C.BLACK, C.KING, C.black_king, 4)
		pieces.append(black_king_piece)
		pieces.append(Piece(C.BLACK, C.BISHOP, C.black_bishop, 5))
		pieces.append(Piece(C.BLACK, C.KNIGHT, C.black_knight, 6))
		pieces.append(Piece(C.BLACK, C.ROOK, C.black_rook, 7))

		pieces.append(Piece(C.WHITE, C.ROOK, C.white_rook, 56))
		pieces.append(Piece(C.WHITE, C.KNIGHT, C.white_knight, 57))
		pieces.append(Piece(C.WHITE, C.BISHOP, C.white_bishop, 58))
		pieces.append(Piece(C.WHITE, C.QUEEN, C.white_queen, 59))
		white_king_piece = Piece(C.WHITE, C.KING, C.white_king, 60)
		pieces.append(white_king_piece)
		pieces.append(Piece(C.WHITE, C.BISHOP, C.white_bishop, 61))
		pieces.append(Piece(C.WHITE, C.KNIGHT, C.white_knight, 62))
		pieces.append(Piece(C.WHITE, C.ROOK, C.white_rook, 63))

		for piece in pieces:
			self.board[piece.position] = piece
		return (white_king_piece, black_king_piece)
	
	def print_board(self):
		for row in self.board[::-1]:
			print(row)




game2 = Game()
game2.play()


