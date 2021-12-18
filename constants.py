import pygame

class Constants:
	PAWN = 1
	BISHOP = 2
	KNIGHT = 3
	ROOK = 4
	QUEEN = 5
	KING = 6

	WHITE = 1
	BLACK = 0

	KINGS_SIDE = 1
	QUEENS_SIDE = 2

	LEFT_CLICK = 1

	BOARD_SIZE = 600
	SQUARE_SIZE = BOARD_SIZE/8

	DARK_BROWN = (101, 67, 33)
	LIGHT_BROWN = (188, 158, 130)
	BLACK = (0, 0, 0)
	OPACITY = 150

	ONGOING = 0
	BLACK_WIN = 1
	WHITE_WIN = 2
	DRAW = 3

	TEXT_TO_PIECE = {"pawn": 1, "bishop": 2,
					 "knight": 3, "rook": 4, 
					 "queen": 5,  "king": 6}

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

	PIECE_TO_IMAGE_WHITE = {1: white_pawn, 2: white_bishop, 3: white_knight,
							4: white_rook, 5: white_queen, 6: white_king}

	PIECE_TO_IMAGE_BLACK = {1: black_pawn, 2: black_bishop, 3: black_knight,
							4: black_rook, 5: black_queen, 6: black_king}

	PIECE_TO_IMAGE = {WHITE: PIECE_TO_IMAGE_WHITE, BLACK: PIECE_TO_IMAGE_BLACK}
