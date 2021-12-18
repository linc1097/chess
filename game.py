import pygame
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
from move import Move
from player import Player, HumanPlayer

class Game:

	board = [[None]*8 for _ in range(8)]
	progress_num = 0

	def move(self, move):
		if move.en_passant:
			if move.piece.color == C.WHITE:
				self.board[move.x][move.y+1] = None
			else:
				self.board[move.x][move.y-1] = None

		if move.castle:
			if move.castle == C.KINGS_SIDE:
				self.board[5][move.y] = self.board[7][move.y]
				self.board[5][move.y].x = 5
				self.board[5][move.y].y = move.y
				self.board[7][move.y] = None
			else:
				self.board[3][move.y] = self.board[0][move.y]
				self.board[3][move.y].x = 3
				self.board[3][move.y].y = move.y
				self.board[0][move.y] = None

		if move.promote:
			move.piece.promote(move.promote)

		self.board[move.x][move.y] = move.piece
		return move.piece.move(move)

	#given king of player whose turn it is
	def game_over(self, king, positions, made_progress):
		legal_moves = Utils.all_legal_moves(self.board, king.color, king = king, attack = False)
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
		return self.board[move.x][move.y] or move.piece.kind == C.PAWN
					
	def play(self):
		white_king, black_king = game2.setup_game()
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')
		positions = {}


		dragging = False
		moving_piece = None
		running = True
		x = 0
		y = 0
		white = HumanPlayer(color = C.WHITE, king = white_king)
		black = HumanPlayer(color = C.BLACK, king = black_king)
		en_passant = None
		made_progress = [False, False]
		while running:
			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			if self.game_over(white_king, positions, made_progress):
				print("GAMEOVER")
				break

			move = white.make_move(screen, self.board)
			made_progress[0] = self.makes_progress(move)

			if en_passant:
				en_passant.en_passant = False
			en_passant = self.move(move)

			Utils.draw_board(screen)
			Utils.draw_pieces(screen, self.board)
			pygame.display.update()

			if self.game_over(black_king, positions, made_progress):
				print("GAMEOVER")
				break

			move = black.make_move(screen, self.board)
			made_progress[1] = self.makes_progress(move)


			if en_passant:
				en_passant.en_passant = False
			en_passant = self.move(move)


	def setup_game(self):
		pieces = []
		for i in range(8):
			pieces.append(Piece(C.BLACK, C.PAWN, C.black_pawn, i, 1))
			pieces.append(Piece(C.WHITE, C.PAWN, C.white_pawn, i, 6))

		pieces.append(Piece(C.BLACK, C.ROOK, C.black_rook, 0, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, C.black_knight, 1, 0))
		pieces.append(Piece(C.BLACK, C.BISHOP, C.black_bishop, 2, 0))
		pieces.append(Piece(C.BLACK, C.QUEEN, C.black_queen, 3, 0))
		black_king_piece = Piece(C.BLACK, C.KING, C.black_king, 4, 0)
		pieces.append(black_king_piece)
		pieces.append(Piece(C.BLACK, C.BISHOP, C.black_bishop, 5, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, C.black_knight, 6, 0))
		pieces.append(Piece(C.BLACK, C.ROOK, C.black_rook, 7, 0))

		pieces.append(Piece(C.WHITE, C.ROOK, C.white_rook, 0, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, C.white_knight, 1, 7))
		pieces.append(Piece(C.WHITE, C.BISHOP, C.white_bishop, 2, 7))
		pieces.append(Piece(C.WHITE, C.QUEEN, C.white_queen, 3, 7))
		white_king_piece = Piece(C.WHITE, C.KING, C.white_king, 4, 7)
		pieces.append(white_king_piece)
		pieces.append(Piece(C.WHITE, C.BISHOP, C.white_bishop, 5, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, C.white_knight, 6, 7))
		pieces.append(Piece(C.WHITE, C.ROOK, C.white_rook, 7, 7))

		for piece in pieces:
			self.board[piece.x][piece.y] = piece
		return (white_king_piece, black_king_piece)
	
	def print_board(self):
		for row in self.board[::-1]:
			print(row)




game2 = Game()
game2.play()


