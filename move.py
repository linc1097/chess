from piece import Piece
from constants import Constants as C

class Move:

	promote = 0
	castle = False
	en_passant = False
	piece = None
	x = 0
	y = 0

	def __init__(self, piece, x, y, promote = 0, castle = False, en_passant = False):
		self.promote = promote
		self.castle = castle
		self.en_passant = en_passant
		self.piece = piece
		self.x = x
		self.y = y

	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ')'