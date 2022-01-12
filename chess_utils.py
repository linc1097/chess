import pygame
import math
import copy
from constants import Constants as C
from piece import Piece
from move import Move

class Utils:

	@staticmethod
	def print_board(board):
		i = 0
		for piece in board:
			if i%8 == 0:
				print('')
			if piece:
				print(piece, end='')
			else: 
				print('0000', end='')
			i += 1
		print('')


	@staticmethod
	def contains_same_coordinates(moves, position):
		for move in moves:
			if move.position == position:
				return move
		return None

	@staticmethod
	def pixel_to_board_coord(pixel_x, pixel_y):
		board_x = pixel_x/C.SQUARE_SIZE
		board_y = pixel_y/C.SQUARE_SIZE
		return math.floor(board_y)*8 + math.floor(board_x)

	@staticmethod
	def highlight_moves(screen, moves):
		for move in moves:
			rect = pygame.Rect(C.SQUARE_SIZE*(move.position%8), C.SQUARE_SIZE*(move.position//8), C.SQUARE_SIZE, C.SQUARE_SIZE)
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
		for i in range(64):
				if board[i]:
					board[i].draw(screen)

	@staticmethod
	def opposing_color(color):
		if color == C.WHITE:
			return C.BLACK
		else:
			return C.WHITE

	@staticmethod
	def all_legal_moves(board, color, attack = False, check = False):
		moves = []
		for piece in board:
			if piece:
				if piece.color == color:
					moves.extend(Utils.piece_moves(board, piece, attack = attack))

		return moves

	@staticmethod
	def move_result(move, board):
		new_board = board[:]
		new_board[move.piece.position] = None
		new_board[move.position] = move.piece
		return new_board

	@staticmethod
	def is_attacked(board, piece):
		attacked_squares = Utils.all_legal_moves(board, Utils.opposing_color(piece.color), attack = True)
		return Utils.contains_same_coordinates(attacked_squares, piece.position)

	@staticmethod
	def is_king_attacked(board, color):
		attacked_squares = Utils.all_legal_moves(board, Utils.opposing_color(color), attack = True)
		for move in attacked_squares:
			piece = board[move.position]
			if piece:
				if piece.kind == C.KING and piece.color == color:
					return True
		return False


	@staticmethod
	def piece_moves(board, piece, attack = False):
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
				if not Utils.is_king_attacked(new_board, piece.color):
					moves.append(move)
		else:
			moves = potential_moves

		return moves


	@staticmethod
	def pawn_moves(board, piece, attack = False):
		position = piece.position
		x = position%8
		y = position//8
		color = piece.color

		moves = []
		if color == C.WHITE:
			if not attack:
				if not piece.moved:
					if position-8 >= 0 and not board[position-8]:
						moves.append(Move(piece, position-8))
						if position-16 >= 0 and not  board[position-16]:
							moves.append(Move(piece, position-16))
				else:
					if not board[position-8]:
						if y-1 == 0:
							for i in range(2, 6, 1):
								moves.append(Move(piece, position-8, promote = i))
						else:
							moves.append(Move(piece, position-8))
			if x+1 <= 7:
				if board[position-7] and board[position-7].color != color:
					if y-1 == 0:
						for i in range(2, 6, 1):
							moves.append(Move(piece, position-7, promote = i))
					else:
						moves.append(Move(piece, position-7))
				elif board[position+1] and board[position+1].color != color:
					if board[position+1].en_passant:
						moves.append(Move(piece, position-7, en_passant = True))
				elif attack:
					moves.append(Move(piece, position-7))
			if x-1 >= 0:
				if board[position-9] and board[position-9].color != color:
					if y-1 == 0:
						for i in range(2, 6, 1):
							moves.append(Move(piece, position-9, promote = i))
					else:
						moves.append(Move(piece, position-9))
				elif board[position-1] and board[position-1].color != color:
					if board[position-1].en_passant:
						moves.append(Move(piece, position-9, en_passant = True))
				elif attack:
					moves.append(Move(piece, position-9))
		else: #if color == black:
			if not attack:
				if not piece.moved:
					if position+8 < 64 and not board[position+8]:
						moves.append(Move(piece, position+8))
						if position+16 < 64 and not  board[position+16]:
							moves.append(Move(piece, position+16))
				else:
					if not board[position+8]:
						if y+1 == 7:
							for i in range(2, 6, 1):
								moves.append(Move(piece, position+8, promote = i))
						else:
							moves.append(Move(piece, position+8))
			if x+1 <= 7:
				if board[position+9] and board[position+9].color != color:
					if y+1 == 7:
						for i in range(2, 6, 1):
							moves.append(Move(piece, position+9, promote = i))
					else:
						moves.append(Move(piece, position+9))
				elif board[position+1] and board[position+1].color != color:
					if board[position+1].en_passant:
						moves.append(Move(piece, position+9, en_passant = True))
				elif attack:
					moves.append(Move(piece, position+9))
			if x-1 >= 0:
				if board[position+7] and board[position+7].color != color:
					if y+1 == 7:
						for i in range(2, 6, 1):
							moves.append(Move(piece, position+7, promote = i))
					else:
						moves.append(Move(piece, position+7))
				elif board[position-1] and board[position-1].color != color:
					if board[position-1].en_passant:
						moves.append(Move(piece, position+7, en_passant = True))
				elif attack:
					moves.append(Move(piece, position+7))

		return moves

	@staticmethod
	def king_moves(board, piece, attack = False):
		position = piece.position
		color = piece.color
		right = position%8 == 7
		left = position%8 == 0
		top = position//8 == 7
		bottom = position//8 == 0


		if left:
			if bottom:
				moves = [position+1, position+8, position+9]
			elif top:
				moves = [position+1, position-8, position-7]
			else:
				moves = [position+1, position-7, position+8, position-8, position+9]
		elif right:
			if bottom:
				moves = [position-1, position+8, position+7]
			elif top:
				moves = [position-1, position-8, position-9]
			else:
				moves = [position-1, position-9, position+8, position-8, position+7]
		elif top:
			moves = [position-1, position+1, position-7, position-8, position-9]
		elif bottom:
			moves = [position-1, position+1, position+7, position+8, position+9]
		else:
			moves = [position+1, position-1, position+7, position-7, position+8, position-8, position+9, position-9]

		valid_moves = []

		for move in moves:
			if board[move]:
				if board[move].color == color:
					if attack:
						valid_moves.append(Move(piece, move))
				else:
					valid_moves.append(Move(piece, move))
			else:
				valid_moves.append(Move(piece, move))

		if not attack:
			attacked_squares = Utils.all_legal_moves(board, Utils.opposing_color(piece.color), attack = True)

			moves = []
			for move in valid_moves:
				if not Utils.contains_same_coordinates(attacked_squares, move.position):
					moves.append(move)
			valid_moves = moves

			if not piece.moved:
				if board[position//8 + 7] and not board[position//8 + 7].moved:
					if not board[position+1] and not board[position+2]:
						if (not Utils.contains_same_coordinates(attacked_squares, position) # could improve performance
							and not Utils.contains_same_coordinates(attacked_squares, position+1) 
							and not Utils.contains_same_coordinates(attacked_squares, position+2)):
							valid_moves.append(Move(piece, position+2, castle = C.KINGS_SIDE))
				if board[position//8] and not board[position//8].moved:
					if not board[position-1] and not board[position-2]:
						if (not Utils.contains_same_coordinates(attacked_squares, position) 
							and not Utils.contains_same_coordinates(attacked_squares, position-1) 
							and not Utils.contains_same_coordinates(attacked_squares, position-2)):
							valid_moves.append(Move(piece, position-2, castle = C.QUEENS_SIDE))
		return valid_moves

	@staticmethod
	def knight_moves(board, piece, attack = False):
		position = piece.position
		x = position%8
		y = position//8
		color = piece.color

		moves = [(x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
				 (x+1, y+2), (x-1, y+2), (x+1, y-2), (x-1, y-2)]

		valid_moves = []

		for move in moves:
			if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0:
				continue
			else:
				move_position =  8*move[1] + move[0]
				if board[move_position]:
					if board[move_position].color == color:
						if attack:
							valid_moves.append(Move(piece, move_position))
					else:
						valid_moves.append(Move(piece, move_position))
				else:
					valid_moves.append(Move(piece, move_position))

		return valid_moves

	@staticmethod
	def bishop_moves(board, piece, attack = False):
		position = piece.position
		color = piece.color

		moves = []
		if position%8 < 7 and position//8 < 7:
			for i in range(1,8,1):
				new_pos = position+(i*9)
				if board[new_pos]:
					if board[new_pos].color == color:
						if attack:
							moves.append(Move(piece, new_pos))
						break
					else:
						moves.append(Move(piece, new_pos))
						if board[new_pos].kind != C.KING:
							break
				else:
					moves.append(Move(piece, new_pos))
				
				if new_pos%8 == 7 or new_pos//8 == 7:
						break
		if position%8 > 0 and position//8 < 7:
			for i in range(1,8,1):
				new_pos = position+(i*7)

				if board[new_pos]:
					if board[new_pos].color == color:
						if attack:
							moves.append(Move(piece, new_pos))
						break
					else:
						moves.append(Move(piece, new_pos))
						if board[new_pos].kind != C.KING:
							break
				else:
					moves.append(Move(piece, new_pos))

				if new_pos%8 == 0 or new_pos//8 == 7:
					break

		if position%8 > 0 and position//8 > 0:
			for i in range(1,8,1):
				new_pos = position-(i*9)

				if board[new_pos]:
					if board[new_pos].color == color:
						if attack:
							moves.append(Move(piece, new_pos))
						break
					else:
						moves.append(Move(piece, new_pos))
						if board[new_pos].kind != C.KING:
							break
				else:
					moves.append(Move(piece, new_pos))

				if new_pos%8 == 0 or new_pos//8 == 0:
					break

		if position%8 < 7 and position//8 > 0:
			for i in range(1,8,1):
				new_pos = position-(i*7)

				if board[new_pos]:
					if board[new_pos].color == color:
						if attack:
							moves.append(Move(piece, new_pos))
						break
					else:
						moves.append(Move(piece, new_pos))
						if board[new_pos].kind != C.KING:
							break
				else:
					moves.append(Move(piece, new_pos))

				if new_pos%8 == 7 or new_pos//8 == 0:
					break
		return moves

	@staticmethod
	def rook_moves(board, piece, attack = False):
		position = piece.position
		color = piece.color

		moves = []
		for i in range(1,8,1):
			new_pos = position+i
			if new_pos%8 == 0:
				break
			elif board[new_pos]:
				if board[new_pos].color == color:
					if attack:
						moves.append(Move(piece, new_pos))
					break
				else:
					moves.append(Move(piece, new_pos))
					if board[new_pos].kind != C.KING:
						break
			else:
				moves.append(Move(piece, new_pos))

		for i in range(1,8,1):
			new_pos = position-i
			if new_pos%8 == 7:
				break
			elif board[new_pos]:
				if board[new_pos].color == color:
					if attack:
						moves.append(Move(piece, new_pos))
					break
				else:
					moves.append(Move(piece, new_pos))
					if board[new_pos].kind != C.KING:
						break
			else:
				moves.append(Move(piece, new_pos))

		for i in range(1,8,1):
			new_pos = position+(8*i)
			if new_pos > 63:
				break
			elif board[new_pos]:
				if board[new_pos].color == color:
					if attack:
						moves.append(Move(piece, new_pos))
					break
				else:
					moves.append(Move(piece, new_pos))
					if board[new_pos].kind != C.KING:
						break
			else:
				moves.append(Move(piece, new_pos))

		for i in range(1,8,1):
			new_pos = position-(i*8)
			if new_pos < 0:
				break
			elif board[new_pos]:
				if board[new_pos].color == color:
					if attack:
						moves.append(Move(piece, new_pos))
					break
				else:
					moves.append(Move(piece, new_pos))
					if board[new_pos].kind != C.KING:
						break
			else:
				moves.append(Move(piece, new_pos))

		return moves
