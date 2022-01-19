import pygame
import chess

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

	PIECE_VALUE = {'p': -100, 'b': -300, 'n': -300, 'r': -500, 'q': -900, 'k': 0, 
				   'P': 100, 'B': 300, 'N': 300, 'R': 500, 'Q': 900, 'K': 0}

	RESULT = {1: "Black Wins!", 2: "White Wins!", 3: "Draw"}

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

	SQUARE_TO_COORDINATE = {chess.A8: (0,0), chess.B8: (1,0), chess.C8: (2,0), chess.D8: (3,0), chess.E8: (4,0), chess.F8: (5,0), chess.G8: (6,0), chess.H8: (7,0), 
							chess.A7: (0,1), chess.B7: (1,1), chess.C7: (2,1), chess.D7: (3,1), chess.E7: (4,1), chess.F7: (5,1), chess.G7: (6,1), chess.H7: (7,1), 
							chess.A6: (0,2), chess.B6: (1,2), chess.C6: (2,2), chess.D6: (3,2), chess.E6: (4,2), chess.F6: (5,2), chess.G6: (6,2), chess.H6: (7,2), 
							chess.A5: (0,3), chess.B5: (1,3), chess.C5: (2,3), chess.D5: (3,3), chess.E5: (4,3), chess.F5: (5,3), chess.G5: (6,3), chess.H5: (7,3), 
							chess.A4: (0,4), chess.B4: (1,4), chess.C4: (2,4), chess.D4: (3,4), chess.E4: (4,4), chess.F4: (5,4), chess.G4: (6,4), chess.H4: (7,4), 
							chess.A3: (0,5), chess.B3: (1,5), chess.C3: (2,5), chess.D3: (3,5), chess.E3: (4,5), chess.F3: (5,5), chess.G3: (6,5), chess.H3: (7,5), 
							chess.A2: (0,6), chess.B2: (1,6), chess.C2: (2,6), chess.D2: (3,6), chess.E2: (4,6), chess.F2: (5,6), chess.G2: (6,6), chess.H2: (7,6), 
							chess.A1: (0,7), chess.B1: (1,7), chess.C1: (2,7), chess.D1: (3,7), chess.E1: (4,7), chess.F1: (5,7), chess.G1: (6,7), chess.H1: (7,7)
							     }

	COORDINATE_TO_SQUARE = {v: k for k, v in SQUARE_TO_COORDINATE.items()}

	PIECE_TO_IMAGE_API = {'P': white_pawn, 'B': white_bishop, 'N': white_knight,
					  'R': white_rook, 'Q': white_queen, 'K': white_king,
					  'p': black_pawn, 'b': black_bishop, 'n': black_knight,
					  'r': black_rook, 'q': black_queen, 'k': black_king	}
