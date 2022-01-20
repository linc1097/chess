import pygame
from constants import Constants as C
import random
import time
import chess
import math
import copy


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

class RandomPlayer(Player):
	
	def make_move(self, board, screen = None):
		possible_moves = board.legal_moves
		return random.choice(list(possible_moves))

class HumanPlayer(Player):

	def position_to_coordinates(self, position):
		return (position%8, position//8)

	def pixel_to_board_coord(self, pixel_x, pixel_y):
		board_x = pixel_x/C.SQUARE_SIZE
		board_y = pixel_y/C.SQUARE_SIZE
		return math.floor(board_y)*8 + math.floor(board_x)

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

	def make_move(self, board_original, screen = None):
		board = copy.copy(board_original)
		running = True
		dragging = False
		moves = []
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == C.LEFT_CLICK:
						if not dragging:
							mouse_x, mouse_y = event.pos
							moving_piece_coord = self.position_to_coordinates(self.pixel_to_board_coord(mouse_x, mouse_y))
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
							new_coordinates = self.position_to_coordinates(self.pixel_to_board_coord(mouse_x, mouse_y))
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


class MiniMaxPlayer(Player):

	num_eval = 0
	depth = 4

	def is_draw(self, board):
		return board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw()

	def num_squares_controlled(self, board, color):
		num_squares = 0
		for square in chess.SQUARES:
			if board.is_attacked_by(color, square):
				num_squares += 1
		return num_squares

	def difference_in_square_control(self, board):
		return self.num_squares_controlled(board, self.color) - self.num_squares_controlled(board, not self.color)


	def material_count(self, board):
		evaluation = 0
		board_string = str(board)
		for char in board_string:
			if char in C.PIECE_VALUE:
				evaluation += C.PIECE_VALUE[char]
		if self.color == chess.BLACK:
			evaluation *= -1
		return evaluation

	def is_passed_pawn(self, piece, piece_square, board):
		if piece.color == chess.WHITE:
			mult = 1
		else:
			mult = -1

		right_edge = piece_square % 8 == 7
		left_edge = piece_square % 8 == 0

		for i in range(1,8,1):
			square_ahead = piece_square+(8*mult*i)
			if square_ahead < 0 or square_ahead > 63:
				break
			squares = [square_ahead]
			if not left_edge:
				squares.append(square_ahead-1)
			if not right_edge:
				squares.append(square_ahead+1)
			for square in squares:
				piece_ahead = board.piece_at(square)
				if piece_ahead and piece_ahead.piece_type == chess.PAWN and piece_ahead.color != piece.color:
					return False

		return True

	def passed_pawn_heuristic(self, board):
		total = 0
		for square in chess.SQUARES:
			piece = board.piece_at(square)
			if piece and piece.piece_type == chess.PAWN:
				if self.is_passed_pawn(piece, square, board):
					if piece.color == self.color:
						total += 1
					else:
						total -= 1

		return total*30

	def evaluate_board(self, board):
		self.num_eval += 1
		return self.material_count(board)

	def allows_tie(self, board):
		moves = board.legal_moves
		for move in moves:
			board.push(move)
			if self.is_draw(board):
				board.pop()
				return True
			else:
				board.pop()


	def make_move(self, board, screen = None):
		start = time.time()
		self.num_eval = 0
		num, best_move = self.make_move_helper(board, self.depth, True)
		end = time.time()
		print('time: ' + str(end-start))
		print('moves: ' + str(self.num_eval))
		print('ratio: ' + str(self.num_eval/(end-start)))

		if self.evaluate_board(board) >= 0:
			board.push(best_move)
			if self.is_draw(board):
				board.pop()
				num, best_move =  self.make_move_helper(board, self.depth, True, forbidden_move=best_move)
			elif self.allows_tie(board):
				board.pop()
				num, best_move =  self.make_move_helper(board, self.depth, True, forbidden_move=best_move)
			else:
				board.pop()
				
		return best_move

	def attacked_by_pawn(self, color, square, board):
		attacked_by = board.attackers(color, square)
		for attacker in attacked_by:
			if board.piece_at(attacker).piece_type == chess.PAWN:
				return True
		return False

	def order_moves(self, moves, board, color):
		first = []
		second = []
		third = []
		fourth = []
		for move in moves:
			piece = board.piece_at(move.from_square)
			take_piece = board.piece_at(move.to_square)
			if piece.piece_type != chess.PAWN:
				if self.attacked_by_pawn(not color, move.to_square, board):
					fourth.append(move)
					continue

			if take_piece:
				if C.PIECE_VALUE[piece.symbol()] < C.PIECE_VALUE[take_piece.symbol()]:
					first.append(move)
				else:
					second.append(move)
			else:
				fourth.append(move)
		first.extend(second)
		first.extend(third)
		first.extend(fourth)
		return first


	def make_move_helper(self, board, depth, maximizing_player, alpha = -20000, beta = 20000, forbidden_move=None):
		if depth == 0:
			return (self.evaluate_board(board), None)

		if maximizing_player:
			moves = self.order_moves(board.legal_moves, board, self.color)
			if forbidden_move:
				moves.remove(forbidden_move)
			if not moves:
				if board.is_check():
					return (-10000, None)
				else:
					return (0, None)
			best = -10001
			best_move = None
			for move in moves:
				board.push(move)
				num, x = self.make_move_helper(board, depth-1, False, alpha = alpha, beta = beta)
				board.pop()
				if num > alpha:
					alpha = num
				if num > best:
					best = num
					best_move = move
				if beta <= alpha:
					break
			return (best, best_move)
		else: 
			moves = self.order_moves(board.legal_moves, board, not self.color)

			if not moves:
				if board.is_check():
					return (10000, None)
				else:
					return (0, None)
			worst = 10001
			worst_move = None
			for move in moves:
				board.push(move)
				num, x = self.make_move_helper(board, depth-1, True, alpha = alpha, beta = beta)
				board.pop()
				if num < beta:
					beta = num
				if num < worst:
					worst = num
					worst_move = move
				if beta <= alpha:
					break
			return (worst, worst_move)

class MiniMaxEvalOnePlayer(MiniMaxPlayer):

	def evaluate_board(self, board):
		self.num_eval += 1
		material_count = self.material_count(board)
		return (material_count + self.difference_in_square_control(board) + self.passed_pawn_heuristic(board))

class MiniMaxEvalTwoPlayer(MiniMaxPlayer):

	def evaluate_board(self, board):
		self.num_eval += 1
		material_count = self.material_count(board)
		return (material_count + self.difference_in_square_control(board))


