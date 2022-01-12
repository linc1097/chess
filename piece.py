from constants import Constants as C

class Piece:
	image = None
	color = -1
	kind = 0
	position = 0
	moved = False
	en_passant = False

	def __init__(self, color, kind, image, position):
		self.color = color
		self.kind = kind
		self.image = image
		self.position = position

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

		string += str(self.position%8) + str(self.position//8)
		return string

	def draw(self, screen, position = None):
		if not position:
			position = self.position
		
		x = (self.position%8)*C.SQUARE_SIZE
		y = (self.position//8)*C.SQUARE_SIZE

		screen.blit(self.image, (x, y))

	def draw_at(self, screen, x, y):
		screen.blit(self.image, (x, y))

	def move(self, move):
		if not self.moved:
			self.moved = True
		if self.kind == C.PAWN:
			if abs(self.position - move.position) > 9:
				self.en_passant = True
				self.position = move.position
				return self
		self.position = move.position
		return None

	def promote(self, promote):
		if promote:
			self.kind = promote
			self.image = C.PIECE_TO_IMAGE[self.color][promote]


