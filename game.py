import pygame

class Game:
	PAWN = 1
	BISHOP = 2
	KNIGHT = 3
	ROOK = 4
	QUEEN = 5
	KING = 6

	WHITE = 1
	BLACK = 0

	BOARD_SIZE = 600
	SQUARE_SIZE = BOARD_SIZE/8

	board = [[(0,0)]*8 for _ in range(8)]

	white_king = pygame.image.load('images/white_king.png')
	white_king = pygame.transform.scale(white_king, (SQUARE_SIZE, SQUARE_SIZE))
	white_queen = pygame.image.load('images/white_queen.png')
	white_queen = pygame.transform.scale(white_queen, (SQUARE_SIZE, SQUARE_SIZE))
	white_rook = pygame.image.load('images/white_rook.png')
	white_rook = pygame.transform.scale(white_rook, (SQUARE_SIZE, SQUARE_SIZE))
	white_knight = pygame.image.load('images/white_knight.png')
	white_knight = pygame.transform.scale(white_knight, (SQUARE_SIZE, SQUARE_SIZE))
	white_bishop = pygame.image.load('images/white_bishop.png')
	white_bishop = pygame.transform.scale(white_bishop, (SQUARE_SIZE, SQUARE_SIZE))
	white_pawn = pygame.image.load('images/white_pawn.png')
	white_pawn = pygame.transform.scale(white_pawn, (SQUARE_SIZE, SQUARE_SIZE))

	black_king = pygame.image.load('images/black_king.png')
	black_king = pygame.transform.scale(black_king, (SQUARE_SIZE, SQUARE_SIZE))
	black_queen = pygame.image.load('images/black_queen.png')
	black_queen = pygame.transform.scale(black_queen, (SQUARE_SIZE, SQUARE_SIZE))
	black_rook = pygame.image.load('images/black_rook.png')
	black_rook = pygame.transform.scale(black_rook, (SQUARE_SIZE, SQUARE_SIZE))
	black_knight = pygame.image.load('images/black_knight.png')
	black_knight = pygame.transform.scale(black_knight, (SQUARE_SIZE, SQUARE_SIZE))
	black_bishop = pygame.image.load('images/black_bishop.png')
	black_bishop = pygame.transform.scale(black_bishop, (SQUARE_SIZE, SQUARE_SIZE))
	black_pawn = pygame.image.load('images/black_pawn.png')
	black_pawn = pygame.transform.scale(black_pawn, (SQUARE_SIZE, SQUARE_SIZE))

	pieces = [[None, white_pawn, white_bishop, white_knight, white_rook, white_queen, white_king],
	[None, black_pawn, black_bishop, black_knight, black_rook, black_queen, black_king]]




	def draw_board(self, screen):
		dark_brown = (101, 67, 33)
		light_brown = (188, 158, 130)
		screen.fill(light_brown)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(game.SQUARE_SIZE*i, game.SQUARE_SIZE*j, game.SQUARE_SIZE, game.SQUARE_SIZE)
					pygame.draw.rect(screen, dark_brown, rect)

	def draw_pieces(self, screen):
		for i in range(8):
			for j in range(8):
				if self.board[i][j] is not (0,0):
					screen.blit(game.pieces[self.board[i][j][1]][self.board[i][j][0]], (game.SQUARE_SIZE*j, game.SQUARE_SIZE*i))




	def play(self):
		pygame.init()
		screen = pygame.display.set_mode((game.BOARD_SIZE, game.BOARD_SIZE))

		pygame.display.set_caption('CHESS')
		icon = pygame.image.load('images/black_king.png')
		pygame.display.set_icon(icon)

		img = pygame.image.load('images/white_king.png')
		img = pygame.transform.scale(img, (game.SQUARE_SIZE, game.SQUARE_SIZE))


		running = True
		while running:
			self.draw_board(screen)
			self.draw_pieces(screen)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			pygame.display.update()

	def setup_game(self):
		self.board[0][0] = (game.ROOK, game.WHITE)
		self.board[0][1] = (game.KNIGHT, game.WHITE)
		self.board[0][2] = (game.BISHOP, game.WHITE)
		self.board[0][3] = (game.QUEEN, game.WHITE)
		self.board[0][4] = (game.KING, game.WHITE)
		self.board[0][5] = (game.BISHOP, game.WHITE)
		self.board[0][6] = (game.KNIGHT, game.WHITE)
		self.board[0][7] = (game.ROOK, game.WHITE)

		self.board[7][0] = (game.ROOK, game.BLACK)
		self.board[7][1] = (game.KNIGHT, game.BLACK)
		self.board[7][2] = (game.BISHOP, game.BLACK)
		self.board[7][3] = (game.QUEEN, game.BLACK)
		self.board[7][4] = (game.KING, game.BLACK)
		self.board[7][5] = (game.BISHOP, game.BLACK)
		self.board[7][6] = (game.KNIGHT, game.BLACK)
		self.board[7][7] = (game.ROOK, game.BLACK)


		for i in range(8):
			self.board[1][i] = (game.PAWN, game.WHITE)
			self.board[6][i] = (game.PAWN, game.BLACK)
	
	def print_board(self):
		for row in self.board[::-1]:
			print(row)




game = Game()
game.setup_game()
game.play()


