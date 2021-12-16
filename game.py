import pygame
import math
from piece import Piece
from constants import Constants as C
from chess_utils import Utils
from move import Move

class Game:

	board = [[None]*8 for _ in range(8)]

	def draw_board(self, screen):
		screen.fill(C.LIGHT_BROWN)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(C.SQUARE_SIZE*i, C.SQUARE_SIZE*j, C.SQUARE_SIZE, C.SQUARE_SIZE)
					pygame.draw.rect(screen, C.DARK_BROWN, rect)


	def draw_pieces(self, screen):
		for i in range(8):
			for j in range(8):
				if self.board[i][j]:
					self.board[i][j].draw(screen)

	def pixel_to_board_coord(self, pixel_x, pixel_y):
		board_x = pixel_x/C.SQUARE_SIZE
		board_y = pixel_y/C.SQUARE_SIZE
		return (int(math.floor(board_x)),int(math.floor(board_y)))

	#def move(self, piece, x, y):
	#	piece.x = x
	#	piece.y = y
	#	self.board[x][y] = piece

	def move(self, move):
		if move.en_passant:
			if move.piece.color == C.WHITE:
				pass
			else:
				pass
		else:
			move.piece.move(move)
			self.board[move.x][move.y] = move.piece

	def highlight_avaialable_moves(self, screen, piece):
		moves = Utils.piece_moves(self.board, piece)
		for move in moves:
			rect = pygame.Rect(C.SQUARE_SIZE*move.x, C.SQUARE_SIZE*move.y, C.SQUARE_SIZE, C.SQUARE_SIZE)
			pygame.draw.rect(screen, C.BLACK, rect)
			#image = pygame.Surface((C.SQUARE_SIZE, C.SQUARE_SIZE))
			#image.set_alpha(C.OPACITY)
			#screen.blit(image, (move.x*C.SQUARE_SIZE, move.y*C.SQUARE_SIZE))


	def play(self):
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')


		dragging = False
		moving_piece = None
		running = True
		x = 0
		y = 0
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == C.LEFT_CLICK:
						if not dragging:
							mouse_x, mouse_y = event.pos
							moving_piece_coord = Game.pixel_to_board_coord(self, mouse_x, mouse_y)
							if self.board[moving_piece_coord[0]][moving_piece_coord[1]]:
								dragging = True
								moving_piece = self.board[moving_piece_coord[0]][moving_piece_coord[1]]
								self.board[moving_piece_coord[0]][moving_piece_coord[1]] = None
								offset_x = moving_piece_coord[0]*C.SQUARE_SIZE - mouse_x
								offset_y = moving_piece_coord[1]*C.SQUARE_SIZE - mouse_y
								x = moving_piece_coord[0]*C.SQUARE_SIZE
								y = moving_piece_coord[1]*C.SQUARE_SIZE

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == C.LEFT_CLICK:
						if dragging:
							mouse_x, mouse_y = event.pos
							new_coordinates = Game.pixel_to_board_coord(self, mouse_x, mouse_y)
							move = Move(moving_piece, new_coordinates[0], new_coordinates[1])
							self.move(move)
							dragging = False
							moving_piece = None

				elif event.type == pygame.MOUSEMOTION:
					if dragging:
						mouse_x, mouse_y = event.pos
						x = mouse_x + offset_x
						y = mouse_y + offset_y

			self.draw_board(screen)
			self.draw_pieces(screen)
			if dragging:
				self.highlight_avaialable_moves(screen, moving_piece)
				moving_piece.draw(screen, x = x, y = y)

			pygame.display.update()

	def setup_game(self):
		white_king = pygame.image.load('images/white_king.png')
		white_king = pygame.transform.scale(white_king, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_queen = pygame.image.load('images/white_queen.png')
		white_queen = pygame.transform.scale(white_queen, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_rook = pygame.image.load('images/white_rook.png')
		white_rook = pygame.transform.scale(white_rook, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_knight = pygame.image.load('images/white_knight.png')
		white_knight = pygame.transform.scale(white_knight, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_bishop = pygame.image.load('images/white_bishop.png')
		white_bishop = pygame.transform.scale(white_bishop, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		white_pawn = pygame.image.load('images/white_pawn.png')
		white_pawn = pygame.transform.scale(white_pawn, (C.SQUARE_SIZE, C.SQUARE_SIZE))

		black_king = pygame.image.load('images/black_king.png')
		black_king = pygame.transform.scale(black_king, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_queen = pygame.image.load('images/black_queen.png')
		black_queen = pygame.transform.scale(black_queen, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_rook = pygame.image.load('images/black_rook.png')
		black_rook = pygame.transform.scale(black_rook, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_knight = pygame.image.load('images/black_knight.png')
		black_knight = pygame.transform.scale(black_knight, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_bishop = pygame.image.load('images/black_bishop.png')
		black_bishop = pygame.transform.scale(black_bishop, (C.SQUARE_SIZE, C.SQUARE_SIZE))
		black_pawn = pygame.image.load('images/black_pawn.png')
		black_pawn = pygame.transform.scale(black_pawn, (C.SQUARE_SIZE, C.SQUARE_SIZE))

		pieces = []
		for i in range(8):
			pieces.append(Piece(C.BLACK, C.PAWN, black_pawn, i, 1))
			pieces.append(Piece(C.WHITE, C.PAWN, white_pawn, i, 6))

		pieces.append(Piece(C.BLACK, C.ROOK, black_rook, 0, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, black_knight, 1, 0))
		pieces.append(Piece(C.BLACK, C.BISHOP, black_bishop, 2, 0))
		pieces.append(Piece(C.BLACK, C.QUEEN, black_queen, 3, 0))
		pieces.append(Piece(C.BLACK, C.KING, black_king, 4, 0))
		pieces.append(Piece(C.BLACK, C.BISHOP, black_bishop, 5, 0))
		pieces.append(Piece(C.BLACK, C.KNIGHT, black_knight, 6, 0))
		pieces.append(Piece(C.BLACK, C.ROOK, black_rook, 7, 0))

		pieces.append(Piece(C.WHITE, C.ROOK, white_rook, 0, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, white_knight, 1, 7))
		pieces.append(Piece(C.WHITE, C.BISHOP, white_bishop, 2, 7))
		pieces.append(Piece(C.WHITE, C.QUEEN, white_queen, 3, 7))
		pieces.append(Piece(C.WHITE, C.KING, white_king, 4, 7))
		pieces.append(Piece(C.WHITE, C.BISHOP, white_bishop, 5, 7))
		pieces.append(Piece(C.WHITE, C.KNIGHT, white_knight, 6, 7))
		pieces.append(Piece(C.WHITE, C.ROOK, white_rook, 7, 7))

		for piece in pieces:
			self.board[piece.x][piece.y] = piece
	
	def print_board(self):
		for row in self.board[::-1]:
			print(row)




game2 = Game()
game2.setup_game()
game2.print_board()
game2.play()


