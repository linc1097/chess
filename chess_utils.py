import pygame
import math
import copy
from constants import Constants as C
from piece import Piece
from move import Move

class Utils:

	@staticmethod
	def contains_same_coordinates(moves, x, y):
		for move in moves:
			if move.x == x and move.y == y:
				return move
		return None

	@staticmethod
	def pixel_to_board_coord(pixel_x, pixel_y):
		board_x = pixel_x/C.SQUARE_SIZE
		board_y = pixel_y/C.SQUARE_SIZE
		return (int(math.floor(board_x)),int(math.floor(board_y)))

	@staticmethod
	def highlight_moves(screen, moves):
		for move in moves:
			rect = pygame.Rect(C.SQUARE_SIZE*move.x, C.SQUARE_SIZE*move.y, C.SQUARE_SIZE, C.SQUARE_SIZE)
			pygame.draw.rect(screen, C.BLACK, rect)

	@staticmethod
	def draw_board(screen):
		screen.fill(C.LIGHT_BROWN)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(C.SQUARE_SIZE*i, C.SQUARE_SIZE*j, C.SQUARE_SIZE, C.SQUARE_SIZE)
					pygame.draw.rect(screen, C.DARK_BROWN, rect)

	@staticmethod
	def draw_pieces(screen, board):
		for i in range(8):
			for j in range(8):
				if board[i][j]:
					board[i][j].draw(screen)

	@staticmethod
	def opposing_color(color):
		if color == C.WHITE:
			return C.BLACK
		else:
			return C.WHITE

	@staticmethod
	def all_legal_moves(board, color, king, attack = False):
		moves = []
		for row in board:
			for piece in row:
				if piece:
					if piece.color == color:
						moves.extend(Utils.piece_moves(board, piece, king, attack = attack))
		return moves

	@staticmethod
	def move_result(move, board):
		new_board = [row[:] for row in board]
		new_board[move.piece.x][move.piece.y] = None
		new_board[move.x][move.y] = move.piece
		return new_board

	@staticmethod
	def is_attacked(board, piece):
		attacked_squares = Utils.all_legal_moves(board, Utils.opposing_color(piece.color), king = piece, attack = True)
		return Utils.contains_same_coordinates(attacked_squares, piece.x, piece.y)

	@staticmethod
	def piece_moves(board, piece, king, attack = False):
		potential_moves = []
		moves = []

		if piece.kind == C.PAWN:
			potential_moves += Utils.pawn_moves(board, piece, attack = attack)
		elif piece.kind == C.KNIGHT:
			potential_moves += Utils.knight_moves(board, piece, attack = attack)
		elif piece.kind == C.BISHOP:
			potential_moves += Utils.bishop_moves(board, piece, attack = attack)
		elif piece.kind == C.ROOK:
			potential_moves += Utils.rook_moves(board, piece, attack = attack)
		elif piece.kind == C.QUEEN:
			potential_moves += Utils.bishop_moves(board, piece, attack = attack)
			potential_moves += Utils.rook_moves(board, piece, attack = attack)
		elif piece.kind == C.KING:
			return Utils.king_moves(board, piece, attack = attack)

		if not attack:
			for move in potential_moves:
				new_board = Utils.move_result(move, board)
				if not Utils.is_attacked(new_board, king):
					moves.append(move)
		else:
			moves = potential_moves

		return moves


	@staticmethod
	def pawn_moves(board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = []
		if color == C.WHITE:
			if not attack:
				if not piece.moved:
					if not board[x][y-1] and not board[x][y-2]:
						moves.append(Move(piece, x, y-2))
						moves.append(Move(piece, x, y-1))
					elif not board[x][y-1]:
						moves.append(Move(piece, x, y-1))
				else:
					if not board[x][y-1]:
						if y-1 == 0:
							for i in range(2, 6, 1):
								moves.append(Move(piece, x, y-1, promote = i))
						else:
							moves.append(Move(piece, x, y-1))
			if x+1 <= 7:
				if board[x+1][y-1] and board[x+1][y-1].color != color:
					if y-1 == 0:
						for i in range(2, 6, 1):
							moves.append(Move(piece, x+1, y-1, promote = i))
					else:
						moves.append(Move(piece, x+1, y-1))
				elif board[x+1][y] and board[x+1][y].color != color:
					if board[x+1][y].en_passant:
						moves.append(Move(piece, x+1, y-1, en_passant = True))
				elif attack:
					moves.append(Move(piece, x+1, y-1))
			if x-1 >= 0:
				if board[x-1][y-1] and board[x-1][y-1].color != color:
					if y-1 == 0:
						for i in range(2, 6, 1):
							moves.append(Move(piece, x-1, y-1, promote = i))
					else:
						moves.append(Move(piece, x-1, y-1))
				elif board[x-1][y] and board[x-1][y].color != color:
					if board[x-1][y].en_passant:
						moves.append(Move(piece, x-1, y-1, en_passant = True))
				elif attack:
					moves.append(Move(piece, x-1, y-1))
		else: #if color == black:
			if not attack:
				if not piece.moved:
					if not board[x][y+1] and not board[x][y+2]:
						moves.append(Move(piece, x, y+2))
						moves.append(Move(piece, x, y+1))
					elif not board[x][y+1]:
						moves.append(Move(piece, x, y+1))
				else:
					if not board[x][y+1]:
						if y+1 == 7:
							for i in range(2, 6, 1):
								moves.append(Move(piece, x, y+1, promote = i))
						else:
							moves.append(Move(piece, x, y+1))
			if x+1 <= 7:
				if board[x+1][y+1] and board[x+1][y+1].color != color:
					if y+1 == 7:
						for i in range(2, 6, 1):
							moves.append(Move(piece, x+1, y+1, promote = i))
					else:
						moves.append(Move(piece, x+1, y+1))
				elif board[x+1][y] and board[x+1][y].color != color:
					if board[x+1][y].en_passant:
						moves.append(Move(piece, x+1, y+1, en_passant = True))
				elif attack:
					moves.append(Move(piece, x+1, y+1))
			if x-1 >= 0:
				if board[x-1][y+1] and board[x-1][y+1].color != color:
					if y+1 == 7:
						for i in range(2, 6, 1):
							moves.append(Move(piece, x-1, y+1, promote = i))
					else:
						moves.append(Move(piece, x-1, y+1))
				elif board[x-1][y] and board[x-1][y].color != color:
					if board[x-1][y].en_passant:
						moves.append(Move(piece, x-1, y+1, en_passant = True))
				elif attack:
					moves.append(Move(piece, x-1, y+1))

		return moves

	@staticmethod
	def king_moves(board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = [Move(piece, x+1, y+1), Move(piece, x+1, y-1), Move(piece, x-1, y+1), Move(piece, x-1, y-1),
				 Move(piece, x+1, y), Move(piece, x-1, y), Move(piece, x, y+1), Move(piece, x, y-1)]

		valid_moves = []

		for move in moves:
			if move.x > 7 or move.x < 0 or move.y > 7 or move.y < 0:
				continue
			elif board[move.x][move.y]:
				if board[move.x][move.y].color == color:
					if attack:
						valid_moves.append(move)
				else:
					valid_moves.append(move)
			else:
				valid_moves.append(move)

		if not attack:
			attacked_squares = Utils.all_legal_moves(board, Utils.opposing_color(piece.color), king = piece, attack = True)

			moves = []
			for move in valid_moves:
				if not Utils.contains_same_coordinates(attacked_squares, move.x, move.y):
					moves.append(move)
			valid_moves = moves

			if not piece.moved:
				if board[7][piece.y] and not board[7][piece.y].moved:
					if not board[piece.x+1][piece.y] and not board[piece.x+2][piece.y]:
						if (not Utils.contains_same_coordinates(attacked_squares, piece.x, piece.y) # could improve performance
							and not Utils.contains_same_coordinates(attacked_squares, piece.x+1, piece.y) 
							and not Utils.contains_same_coordinates(attacked_squares, piece.x+2, piece.y)):
							valid_moves.append(Move(piece, piece.x+2, piece.y, castle = C.KINGS_SIDE))
				if board[0][piece.y] and not board[0][piece.y].moved:
					if not board[piece.x-1][piece.y] and not board[piece.x-2][piece.y] and not board[piece.x-2][piece.y]:
						if (not Utils.contains_same_coordinates(attacked_squares, piece.x, piece.y) 
							and not Utils.contains_same_coordinates(attacked_squares, piece.x-1, piece.y) 
							and not Utils.contains_same_coordinates(attacked_squares, piece.x-2, piece.y)):
							valid_moves.append(Move(piece, piece.x-2, piece.y, castle = C.QUEENS_SIDE))
		return valid_moves

	@staticmethod
	def knight_moves(board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = [Move(piece, x+2, y+1), Move(piece, x+2, y-1), Move(piece, x-2, y+1), Move(piece, x-2, y-1),
				 Move(piece, x+1, y+2), Move(piece, x-1, y+2), Move(piece, x+1, y-2), Move(piece, x-1, y-2)]

		valid_moves = []

		for move in moves:
			if move.x > 7 or move.x < 0 or move.y > 7 or move.y < 0:
				continue
			elif board[move.x][move.y]:
				if board[move.x][move.y].color == color:
					if attack:
						valid_moves.append(move)
				else:
					valid_moves.append(move)
			else:
				valid_moves.append(move)

		return valid_moves

	@staticmethod
	def bishop_moves(board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = []
		for i in range(1,8,1):
			if x+i > 7 or y+i > 7:
				break
			elif board[x+i][y+i]:
				if board[x+i][y+i].color == color:
					if attack:
						moves.append(Move(piece, x+i, y+i))
					break
				else:
					moves.append(Move(piece, x+i, y+i))
					if board[x+i][y+i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x+i, y+i))

		for i in range(1,8,1):
			if x-i < 0 or y+i > 7:
				break
			elif board[x-i][y+i]:
				if board[x-i][y+i].color == color:
					if attack:
						moves.append(Move(piece, x-i, y+i))
					break
				else:
					moves.append(Move(piece, x-i, y+i))
					if board[x-i][y+i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x-i, y+i))

		for i in range(1,8,1):
			if x+i > 7 or y-i < 0:
				break
			elif board[x+i][y-i]:
				if board[x+i][y-i].color == color:
					if attack:
						moves.append(Move(piece, x+i, y-i))
					break
				else:
					moves.append(Move(piece, x+i, y-i))
					if board[x+i][y-i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x+i, y-i))

		for i in range(1,8,1):
			if x-i < 0 or y-i < 0:
				break
			elif board[x-i][y-i]:
				if board[x-i][y-i].color == color:
					if attack:
						moves.append(Move(piece, x-i, y-i))
					break
				else:
					moves.append(Move(piece, x-i, y-i))
					if board[x-i][y-i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x-i, y-i))

		return moves

	@staticmethod
	def rook_moves(board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = []
		for i in range(1,8,1):
			if x+i > 7:
				break
			elif board[x+i][y]:
				if board[x+i][y].color == color:
					if attack:
						moves.append(Move(piece, x+i, y))
					break
				else:
					moves.append(Move(piece, x+i, y))
					if board[x+i][y].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x+i, y))

		for i in range(1,8,1):
			if x-i < 0:
				break
			elif board[x-i][y]:
				if board[x-i][y].color == color:
					if attack:
						moves.append(Move(piece, x-i, y))
					break
				else:
					moves.append(Move(piece, x-i, y))
					if board[x-i][y].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x-i, y))

		for i in range(1,8,1):
			if y+i > 7:
				break
			elif board[x][y+i]:
				if board[x][y+i].color == color:
					if attack:
						moves.append(Move(piece, x, y+i))
					break
				else:
					moves.append(Move(piece, x, y+i))
					if board[x][y+i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x, y+i))

		for i in range(1,8,1):
			if y-i < 0:
				break
			elif board[x][y-i]:
				if board[x][y-i].color == color:
					if attack:
						moves.append(Move(piece, x, y-i))
					break
				else:
					moves.append(Move(piece, x, y-i))
					if board[x][y-i].kind != C.KING:
						break
			else:
				moves.append(Move(piece, x, y-i))


		return moves
