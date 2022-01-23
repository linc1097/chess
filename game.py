import chess 
import pygame
import time
from player import Player, RandomPlayer, HumanPlayer, MiniMaxPlayer, MiniMaxEvalOnePlayer, MiniMaxEvalTwoPlayer
from constants import Constants as C

class Game:
	board = chess.Board()
	
	def play(self):
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')

		white = HumanPlayer(color = chess.WHITE)
		black = MiniMaxEvalOnePlayer(color = chess.BLACK)
		with open('board_data.txt', 'w') as file:
			while True:
				pygame.event.get()
				self.draw_board(screen, self.board)
				pygame.display.update()

				game_result = self.game_over(black.color, self.board)
				if game_result:
					print(C.RESULT[game_result])
					break
				move = white.make_move(self.board, screen = screen)
				self.board.push(move)

				self.draw_board(screen, self.board)
				pygame.display.update()

				game_result = self.game_over(white.color, self.board)
				if game_result:
					print(C.RESULT[game_result])
					break

				move = black.make_move(self.board, screen = screen)
				self.board.push(move)

	def collect_data(self):
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')

		white = MiniMaxEvalOnePlayer(color = chess.WHITE)
		black = MiniMaxEvalOnePlayer(color = chess.BLACK)
		board = chess.Board()

		moves = board.legal_moves
		with open('board_data.txt', 'w') as file:
			i_0 = 1
			for move in moves:
				board = chess.Board()
				board.push(move)
				i_1 = 1

				while True:
					print(i_1)
					i_1 += 1

					pygame.event.get()
					self.draw_board(screen, board)
					pygame.display.update()

					move = black.make_move(board, file = file)
					board.push(move)

					game_result = self.game_over(black.color, board)
					if game_result:
						print(C.RESULT[game_result])
						break

					pygame.event.get()
					self.draw_board(screen, board)
					pygame.display.update()

					move = white.make_move(board, file = file)
					board.push(move)

					game_result = self.game_over(white.color, board)
					if game_result:
						print(C.RESULT[game_result])
						break

				print('GAME: ' + str(i_0))
				i_0 += 1


	def game_over(self, color, board):
		if board.is_checkmate():
			if color:
				return C.WHITE_WIN
			else:
				return C.BLACK_WIN

		if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
			return C.DRAW


	def draw(self, position, piece_string, screen):
		x = (position%8)*C.SQUARE_SIZE
		y = (position//8)*C.SQUARE_SIZE
		screen.blit(C.PIECE_TO_IMAGE_API[piece_string], (x, y))

	def draw_board(self, screen, board):
		screen.fill(C.LIGHT_BROWN)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(C.SQUARE_SIZE*i, C.SQUARE_SIZE*j, C.SQUARE_SIZE, C.SQUARE_SIZE)
					pygame.draw.rect(screen, C.DARK_BROWN, rect)

		board_string = str(board)
		i = 0
		for char in board_string:
			if char in C.PIECE_TO_IMAGE_API:
				self.draw(i, char, screen)
				i += 1
			elif char == '.':
				i += 1


game = Game()
#game.play()
game.collect_data()

