from constants import Constants as C

class Piece:
	image = None
	color = -1
	kind = 0
	x = 0
	y = 0
	moved = False
	en_passant = False

	def __init__(self, color, kind, image, x, y):
		self.color = color
		self.kind = kind
		self.image = image
		self.x = x
		self.y = y

	def __str__(self):
		if self.color == C.WHITE:
			string = 'W'
		if self.color == C.BLACK:
			string = 'B'

		if self.kind == C.PAWN:
			string += 'P'
		elif self.kind == C.BISHOP:
			string += 'B'
		elif self.kind == C.KNIGHT:
			string += 'N'
		elif self.kind == C.ROOK:
			string += 'R'
		elif self.kind == C.QUEEN:
			string += 'Q'
		elif self.kind == C.KING:
			string += 'K'

		string += str(self.x) + str(self.y)
		return string

	def draw(self, screen, x = None, y = None):
		if not x and not y:
			x = self.x*C.SQUARE_SIZE
			y = self.y*C.SQUARE_SIZE

		screen.blit(self.image, (x, y))

	def move(self, move):
		if not self.moved:
			self.moved = True
		if self.kind == C.PAWN:
			if abs(self.y - move.y) > 1:
				self.en_passant = True
			elif self.en_passant:
				self.en_passant = False
		self.x = move.x
		self.y = move.y

