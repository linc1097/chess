import pygame
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
import random
from move import Move
import time

class Player:
	king = None
	other_king = None
	color = -1

	def __init__(self, color, king, other_king):
		self.color = color
		self.king = king
		self.other_king = other_king

	def make_move(self, board, screen = None):
		pass

class RandomPlayer(Player):

	def make_move(self, board, screen = None):
		possible_moves = Utils.all_legal_moves(board, self.color)
		return random.choice(possible_moves)

class MiniMaxPlayer(Player):

	num_eval = 0

	def evaluate_board_simple(self, board):
		self.num_eval += 1
		evaluation = 0
		for piece in board:
			if piece:
				if piece.color == self.color:
					evaluation += C.PIECE_VALUE[piece.kind]
				else:
					evaluation -= C.PIECE_VALUE[piece.kind]
		return evaluation


	def make_move(self, board, screen = None):
		start = time.time()
		self.num_eval = 0
		moves = self.order_moves(Utils.all_legal_moves(board, self.color), board)
		best_num = -101
		best_move = None
		for move in moves:
			prev_piece = board[move.position]
			prev_position = move.piece.position
			board[move.piece.position] = None
			board[move.position] = move.piece
			move.piece.position = move.position
			num = self.make_move_helper(board, 2, False)
			board[move.position] = prev_piece
			board[prev_position] = move.piece
			move.piece.position = prev_position
			if num > best_num:
				best_num = num
				best_move = move
		end = time.time()
		print('time: ' + str(end-start))
		print('moves: ' + str(self.num_eval))
		print('ratio: ' + str(self.num_eval/(end-start)))


		return best_move

	def order_moves(self, moves, board):
		first = []
		second = []
		third = []
		fourth = []
		for move in moves:
			if board[move.position]:
				if C.PIECE_VALUE[move.piece.kind] < C.PIECE_VALUE[board[move.position].kind]:
					first.append(move)
				else:
					second.append(move)
			elif move.piece.kind == C.PAWN:
				third.append(move)
			else:
				fourth.append(move)
		first.extend(second)
		first.extend(third)
		first.extend(fourth)
		return first

	def make_move_helper(self, board, depth, maximizing_player, alpha = -200, beta = 200):
		if depth == 0:
			return self.evaluate_board_simple(board)

		if maximizing_player:
			moves = self.order_moves(Utils.all_legal_moves(board, self.color), board)
			if not moves:
				if Utils.is_king_attacked(board, self.color):
					return -100
				else:
					return 0
			best = -101
			for move in moves:
				prev_piece = board[move.position]
				prev_position = move.piece.position
				board[move.piece.position] = None
				board[move.position] = move.piece
				move.piece.position = move.position
				num = self.make_move_helper(board, depth-1, False, alpha = alpha, beta = beta)
				board[move.position] = prev_piece
				board[prev_position] = move.piece
				move.piece.position = prev_position
				if num > alpha:
					alpha = num
				if num > best:
					best = num
				if beta <= alpha:
					break
			return best
		else: 
			#moves = Utils.all_legal_moves(board, Utils.opposing_color(self.color), check = True)
			moves = self.order_moves(Utils.all_legal_moves(board, Utils.opposing_color(self.color), check = True), board)

			if not moves:
				if Utils.is_king_attacked(board, Utils.opposing_color(self.color)):
					return 100
				else:
					return 0
			worst = 101
			for move in moves:
				prev_piece = board[move.position]
				prev_position = move.piece.position
				board[move.piece.position] = None
				board[move.position] = move.piece
				move.piece.position = move.position
				num = self.make_move_helper(board, depth-1, True, alpha = alpha, beta = beta)
				board[move.position] = prev_piece
				board[prev_position] = move.piece
				move.piece.position = prev_position
				if num < beta:
					beta = num
				if num < worst:
					worst = num
				if beta <= alpha:
					break
			return worst




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
							if board[moving_piece_coord]:
								moving_piece = board[moving_piece_coord]
								if moving_piece.color == self.color:
									dragging = True
									board[moving_piece_coord] = None
									offset_x = (moving_piece_coord%8)*C.SQUARE_SIZE - mouse_x
									offset_y = (moving_piece_coord//8)*C.SQUARE_SIZE - mouse_y
									x = (moving_piece_coord%8)*C.SQUARE_SIZE
									y = (moving_piece_coord//8)*C.SQUARE_SIZE
									possible_moves = Utils.piece_moves(board, moving_piece, attack=False)

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == C.LEFT_CLICK:
						if dragging:
							mouse_x, mouse_y = event.pos
							new_coordinates = Utils.pixel_to_board_coord(mouse_x, mouse_y)
							move = Utils.contains_same_coordinates(possible_moves, new_coordinates)
							if move:
								if move.promote:
									promote_type = input()
									while promote_type not in C.TEXT_TO_PIECE.keys():
										promote_type = input()
									move.promote = C.TEXT_TO_PIECE[promote_type]
								return move
							else:
								board[moving_piece.position] = moving_piece
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
				moving_piece.draw_at(screen, x = x, y = y)
			pygame.display.update()
