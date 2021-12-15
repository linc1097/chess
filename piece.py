from constants import Constants

class Piece:
	image = None
	color = -1
	kind = 0
	x = 0
	y = 0

	def __init__(self, color, kind, image, x, y):
		self.color = color
		self.kind = kind
		self.image = image
		self.x = x
		self.y = y

	def __str__(self):
		if self.color == Constants.WHITE:
			string = 'W'
		if self.color == Constants.BLACK:
			string = 'B'

		if self.kind == Constants.PAWN:
			string += 'P'
		elif self.kind == Constants.BISHOP:
			string += 'B'
		elif self.kind == Constants.KNIGHT:
			string += 'N'
		elif self.kind == Constants.ROOK:
			string += 'R'
		elif self.kind == Constants.QUEEN:
			string += 'Q'
		elif self.kind == Constants.KING:
			string += 'K'

		string += str(self.x) + str(self.y)
		return string

	def draw(self, screen, x = None, y = None):
		if not x and not y:
			x = self.x*Constants.SQUARE_SIZE
			y = self.y*Constants.SQUARE_SIZE

		screen.blit(self.image, (x, y))

	def move(self, x, y):
		self.x = x
		self.y = y
