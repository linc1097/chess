from constants import Constants as C
from piece import Piece
from move import Move

class Utils:

	def all_legal_moves(self, board, color):
		moves = []
		for row in board:
			for piece in row:
				if piece:

	def legal_moves(self, board, piece):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = []

		if piece.kind == C.PAWN:
			moves.extend(self.pawn_moves(board, piece))
		elif piece.kind == C.KNIGHT:
			moves.extend(self.bishop_moves(board, piece))
		elif piece.kind == C.BISHOP:
			moves.extend(self.bishop_moves(board, piece))
		elif piece.kind == C.ROOK:
			moves.extend(self.rook_moves(board, piece))
		elif piece.kind == C.QUEEN:
			moves.extend(self.bishop_moves(board, piece))
			moves.extend(self.rook_moves(board, piece))
		elif piece.kind == C.KING:
			moves.extend(self.king_moves(board, piece))

		return moves

	def pawn_moves(self, board, piece, attack = False):
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
				else:
					if not board[x][y-1]:
						if y-1 == 0:
							for i in range(2, 6, 1):
								moves.append(Move(piece, x, y-1, promote = i))
						else:
							moves.append(Move(piece, x, y-1))

			if x+1 < 7 and board[x+1][y-1]:
				if y-1 == 0:
					for i in range(2, 6, 1):
						moves.append(Move(piece, x+1, y-1, promote = i))
				else:
					moves.append(Move(piece, x+1, y-1))
			elif board[x+1][y]:
				if board[x+1][y].en_passant:
					moves.append(Move(piece, x+1, y-1, en_passant = True))

			if x-1 > 0 and board[x-1][y-1]:
				if y-1 == 0:
					for i in range(2, 6, 1):
						moves.append(Move(piece, x-1, y-1, promote = i))
				else:
					moves.append(Move(piece, x-1, y-1))
			elif board[x-1][y]:
				if board[x-1][y].en_passant:
					moves.append(Move(piece, x-1, y-1, en_passant = True))
		else: #if color == black:
			if not attack:
				if not piece.moved:
					if not board[x][y+1] and not board[x][y+2]:
						moves.append(Move(piece, x, y+2))
						moves.append(Move(piece, x, y+1))
				else:
					if not board[x][y+1]:
						if y+1 == 7:
							for i in range(2, 6, 1):
								moves.append(Move(piece, x, y+1, promote = i))
						else:
							moves.append(Move(piece, x, y+1))

			if x+1 < 7 and board[x+1][y+1]:
				if y+1 == 7:
					for i in range(2, 6, 1):
						moves.append(Move(piece, x+1, y+1, promote = i))
				else:
					moves.append(Move(piece, x+1, y+1))
			elif board[x+1][y]:
				if board[x+1][y].en_passant:
					moves.append(Move(piece, x+1, y+1, en_passant = True))

			if x-1 > 0 and board[x-1][y+1]:
				if y+1 == 7:
					for i in range(2, 6, 1):
						moves.append(Move(piece, x-1, y+1, promote = i))
				else:
					moves.append(Move(piece, x-1, y+1))
			elif board[x-1][y]:
				if board[x-1][y].en_passant:
					moves.append(Move(piece, x-1, y+1, en_passant = True))

		return moves

	def king_moves(self, board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = [Move(piece, x+1, y+1), Move(piece, x+1, y-1), Move(piece, x-1, y+1), Move(piece, x-1, y-1),
				 Move(piece, x+1, y), Move(piece, x-1, y), Move(piece, x, y+1), Move(piece, x, y-1)]

		valid_moves = []

		for move in moves:
			if move[C.X] > 7 or move[C.X] < 0 or move[C.Y] > 7 or move[C.Y] < 0:
				continue
			elif board[move[C.X]][move[C.Y]]:
				if board[move[C.X]][move[C.Y]].color == color:
					if attack:
						valid_moves.append(move)
				else:
					valid_moves.append(move)
			else:
				valid_moves.append(move)

		return valid_moves

	def knight_moves(self, board, piece, attack = False):
		x = piece.x
		y = piece.y
		color = piece.color

		moves = [Move(piece, x+2, y+1), Move(piece, x+2, y-1), Move(piece, x-2, y+1), Move(piece, x-2, y-1),
				 Move(piece, x+1, y+2), Move(piece, x-1, y+2), Move(piece, x+1, y-2), Move(piece, x-1, y-2)]

		valid_moves = []

		for move in moves:
			if move[C.X] > 7 or move[C.X] < 0 or move[C.Y] > 7 or move[C.Y] < 0:
				continue
			elif board[move[C.X]][move[C.Y]]:
				if board[move[C.X]][move[C.Y]].color == color:
					if attack:
						valid_moves.append(move)
				else:
					valid_moves.append(move)
			else:
				valid_moves.append(move)

		return valid_moves

	def bishop_moves(self, board, piece, attack = False):
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
					break
			else:
				moves.append(Move(piece, x-i, y-i))

		return moves

	def rook_moves(self, board, piece, attack = False):
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
					break
			else:
				moves.append(Move(piece, x, y-i))


		return moves
