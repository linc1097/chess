import chess 
import pygame
import time
from player import Player, RandomPlayerAPI, HumanPlayerAPI, MiniMaxPlayerAPI
from constants import Constants as C

class Game:
	board = chess.Board()
	
	def play(self):
		pygame.init()
		screen = pygame.display.set_mode((C.BOARD_SIZE, C.BOARD_SIZE))
		pygame.display.set_caption('CHESS')

		white = HumanPlayerAPI(color = chess.WHITE)
		black = MiniMaxPlayerAPI(color = chess.BLACK)
		while True:
			pygame.event.get()
			self.draw_board(screen)
			pygame.display.update()
			time.sleep(0.2)

			game_result = self.game_over(black.color)
			if game_result:
				print(C.RESULT[game_result])
				break

			move = white.make_move(self.board, screen = screen)
			self.board.push(move)
		
			self.draw_board(screen)
			pygame.display.update()
			time.sleep(0.2)

			game_result = self.game_over(white.color)
			if game_result:
				print(C.RESULT[game_result])
				break

			move = black.make_move(self.board, screen = screen)
			self.board.push(move)

	def game_over(self, color):
		if self.board.is_checkmate():
			if color:
				return C.WHITE_WIN
			else:
				return C.BLACK_WIN

		if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
			return C.DRAW


	def draw(self, position, piece_string, screen):
		x = (position%8)*C.SQUARE_SIZE
		y = (position//8)*C.SQUARE_SIZE
		screen.blit(C.PIECE_TO_IMAGE_API[piece_string], (x, y))

	def draw_board(self, screen):
		screen.fill(C.LIGHT_BROWN)

		for i in range(8):
			for j in range(8):
				if (i+j) % 2 == 1:
					rect = pygame.Rect(C.SQUARE_SIZE*i, C.SQUARE_SIZE*j, C.SQUARE_SIZE, C.SQUARE_SIZE)
					pygame.draw.rect(screen, C.DARK_BROWN, rect)

		board_string = str(self.board)
		i = 0
		for char in board_string:
			if char in C.PIECE_TO_IMAGE_API:
				self.draw(i, char, screen)
				i += 1
			elif char == '.':
				i += 1


game = Game()
game.play()

