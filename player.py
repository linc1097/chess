import pygame
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
import random
from move import Move

class Player:
	king = None
	color = -1

	def __init__(self, color, king):
		self.color = color
		self.king = king

	def make_move(self, board, screen = None):
		pass

class RandomPlayer(Player):

	def make_move(self, board, screen = None):
		possible_moves = Utils.all_legal_moves(board, self.color, self.king)
		return random.choice(possible_moves)

class HumanPlayer(Player):

	def make_move(self, board, screen = None):
		running = True
		dragging = False
		moves = []
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == C.LEFT_CLICK:
						if not dragging:
							mouse_x, mouse_y = event.pos
							moving_piece_coord = Utils.pixel_to_board_coord(mouse_x, mouse_y)
							if board[moving_piece_coord[0]][moving_piece_coord[1]]:
								moving_piece = board[moving_piece_coord[0]][moving_piece_coord[1]]
								if moving_piece.color == self.color:
									dragging = True
									board[moving_piece_coord[0]][moving_piece_coord[1]] = None
									offset_x = moving_piece_coord[0]*C.SQUARE_SIZE - mouse_x
									offset_y = moving_piece_coord[1]*C.SQUARE_SIZE - mouse_y
									x = moving_piece_coord[0]*C.SQUARE_SIZE
									y = moving_piece_coord[1]*C.SQUARE_SIZE
									possible_moves = Utils.piece_moves(board, moving_piece, self.king)

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == C.LEFT_CLICK:
						if dragging:
							mouse_x, mouse_y = event.pos
							new_coordinates = Utils.pixel_to_board_coord(mouse_x, mouse_y)
							move = Utils.contains_same_coordinates(possible_moves, new_coordinates[0], new_coordinates[1])
							if move:
								if move.promote:
									promote_type = input()
									while promote_type not in C.TEXT_TO_PIECE.keys():
										promote_type = input()
									move.promote = C.TEXT_TO_PIECE[promote_type]
								return move
							else:
								board[moving_piece.x][moving_piece.y] = moving_piece
								return self.make_move(board, screen = screen)

				elif event.type == pygame.MOUSEMOTION:
					if dragging:
						mouse_x, mouse_y = event.pos
						x = mouse_x + offset_x
						y = mouse_y + offset_y

			Utils.draw_board(screen)
			Utils.draw_pieces(screen, board)
			if dragging:
				Utils.highlight_moves(screen, possible_moves)
				moving_piece.draw(screen, x = x, y = y)
			pygame.display.update()
