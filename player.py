import pygame
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
import random
from move import Move
import time
import chess

class Player:
	king = None
	other_king = None
	color = -1

	def __init__(self, color, king = None, other_king = None):
		self.color = color
		self.king = king
		self.other_king = other_king

	def make_move(self, board, screen = None):
		pass

class RandomPlayerAPI(Player):
	
	def make_move(self, board, screen = None):
		possible_moves = board.legal_moves
		return random.choice(list(possible_moves))

class RandomPlayer(Player):
	
	def make_move(self, board, screen = None):
		possible_moves = Utils.all_legal_moves(board, self.color)
		return random.choice(possible_moves)

class MiniMaxPlayerAPI(Player):

	num_eval = 0

	def evaluate_board_simple(self, board):
		self.num_eval += 1
		evaluation = 0
		board_string = str(board)
		for char in board_string:
			if char in C.PIECE_TO_VALUE_API:
				evaluation += C.PIECE_TO_VALUE_API[char]
		if not self.color:
			evaluation *= -1
		return evaluation


	def make_move(self, board, screen = None):
		start = time.time()
		self.num_eval = 0
		moves = self.order_moves(board.legal_moves, board)
		best_num = -101
		best_move = None
		for move in moves:
			board.push(move)
			num = self.make_move_helper(board, 2, False)
			board.pop()
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
			piece = board.piece_at(move.from_square)
			take_piece = board.piece_at(move.to_square)
			if piece.piece_type != chess.PAWN:
				attackers = board.attackers(not self.color, move.from_square)
				for attacker in attackers:
					if board.piece_at(attacker).piece_type == chess.PAWN:
						first.append(move)
						continue
			if take_piece:
				if C.PIECE_TO_VALUE_API[piece.symbol()] < C.PIECE_TO_VALUE_API[take_piece.symbol()]:
					first.append(move)
				else:
					second.append(move)
			elif piece.piece_type == chess.PAWN:
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
			moves = board.legal_moves
			if not moves:
				if board.is_check():
					return -100
				else:
					return 0
			best = -101
			for move in moves:
				board.push(move)
				num = self.make_move_helper(board, depth-1, False, alpha = alpha, beta = beta)
				board.pop()
				if num > alpha:
					alpha = num
				if num > best:
					best = num
				if beta <= alpha:
					break
			return best
		else: 
			#moves = Utils.all_legal_moves(board, Utils.opposing_color(self.color), check = True)
			moves = board.legal_moves

			if not moves:
				if board.is_check():
					return 100
				else:
					return 0
			worst = 101
			for move in moves:
				board.push(move)
				num = self.make_move_helper(board, depth-1, True, alpha = alpha, beta = beta)
				board.pop()
				if num < beta:
					beta = num
				if num < worst:
					worst = num
				if beta <= alpha:
					break
			return worst

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




class HumanPlayerAPI(Player):

	def draw(self, position, piece_string, screen):
		x = (position%8)*C.SQUARE_SIZE
		y = (position//8)*C.SQUARE_SIZE
		screen.blit(C.PIECE_TO_IMAGE_API[piece_string], (x, y))

	def draw_board(self, screen, board):
		screen.fill(C.LIGHT_BROWN)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(C.SQUARE_SIZE*i, C.SQUARE_SIZE*j, C.SQUARE_SIZE, C.SQUARE_SIZE)
					pygame.draw.rect(screen, C.DARK_BROWN, rect)

		board_string = str(board)
		i = 0
		for char in board_string:
			if char in C.PIECE_TO_IMAGE_API:
				self.draw(i, char, screen)
				i += 1
			elif char == '.':
				i += 1

	def is_move(self, square, possible_moves):
		for move in possible_moves:
			if move.to_square == square:
				return move
		return None

	def highlight_moves(self, moves, screen):
		for move in moves:
			x, y = C.SQUARE_TO_COORDINATE[move.to_square]
			rect = pygame.Rect(C.SQUARE_SIZE*(x), C.SQUARE_SIZE*(y), C.SQUARE_SIZE, C.SQUARE_SIZE)
			pygame.draw.rect(screen, C.BLACK, rect)

	def draw_piece_at(self, screen, piece, x, y):
		screen.blit(C.PIECE_TO_IMAGE_API[piece.symbol()], (x, y))

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
							moving_piece_coord = Utils.position_to_coordinates(Utils.pixel_to_board_coord(mouse_x, mouse_y))
							from_square = C.COORDINATE_TO_SQUARE[moving_piece_coord]
							piece = board.piece_at(from_square)
							if piece and piece.color == self.color:
								moving_piece = piece
								dragging = True
								offset_x = (moving_piece_coord[0])*C.SQUARE_SIZE - mouse_x
								offset_y = (moving_piece_coord[1])*C.SQUARE_SIZE - mouse_y
								x = (moving_piece_coord[0])*C.SQUARE_SIZE
								y = (moving_piece_coord[1])*C.SQUARE_SIZE
								possible_moves = []
								for square in chess.SQUARES:
									try:
										possible_moves.append(board.find_move(from_square=from_square, to_square=square))
									except (ValueError):
										continue
								board.remove_piece_at(from_square)
								
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == C.LEFT_CLICK:
						if dragging:
							mouse_x, mouse_y = event.pos
							new_coordinates = Utils.position_to_coordinates(Utils.pixel_to_board_coord(mouse_x, mouse_y))
							to_square = C.COORDINATE_TO_SQUARE[new_coordinates]
							move = self.is_move(to_square, possible_moves)
							board.set_piece_at(from_square, moving_piece)
							if move:
								return move
							else:
								return self.make_move(board, screen = screen)

				elif event.type == pygame.MOUSEMOTION:
					if dragging:
						mouse_x, mouse_y = event.pos
						x = mouse_x + offset_x
						y = mouse_y + offset_y

			self.draw_board(screen, board)
			if dragging:
				self.highlight_moves(possible_moves, screen)
				self.draw_piece_at(screen, moving_piece, x, y)
			pygame.display.update()

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
