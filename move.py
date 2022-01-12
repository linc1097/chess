from piece import Piece
from constants import Constants as C

class Move:

	promote = 0
	castle = 0
	en_passant = False
	piece = None
	position = 0

	def __init__(self, piece, position, promote = 0, castle = 0, en_passant = False):
		self.promote = promote
		self.castle = castle
		self.en_passant = en_passant
		self.piece = piece
		self.position = position

	def __str__(self):
		return '(' + '(' + str(self.position%8) + ', ' + str(self.position//8)  + ') , ' + str(self.piece) + ')'