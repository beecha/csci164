import sys
from othello import *


def check(move, player, board):
	return isValid(move) and isLegal(move, player, board)
	
def human(player, board):
	print display_board(board)
	print 'Enter your move'
	while True:
		move = raw_input('> ')
		if move and check(int(move), player, board):
			return int(move)
		elif move:
			print 'Move is illegal. Try a different square.'
			
def getChoice(prompt, options):
	print prompt
	print 'Options:', options.keys()
	while True:
		choice = raw_input('> ')
		if choice in options:
			return options[choice]
		elif choice:
			print 'Choice is not valid.'
			
def getPlayers():
	print 'A Game of Othello'
	options = {
				'Human': human,
				
				#---Difficulty Options for the AI---
				'Random': randomApproach,
			  }
	black = getChoice('BLACK player(O): Choose approach', options)
	white = getChoice('WHITE player(X): choose approach', options)
	return black, white
	
	
"""
def main():
	try:
		black, white = getPlayers()
		board, score = play(black, white)
	except IllegalMoveError as err:
		print err
		return
	except EOFError as err:
		print 'Fin'
		return
	print 'Total Score: ', score
	print '%s is the winner' % ('Black' if score > 0 else 'White')
	print display_board(board)

if __name__ == "__main__":
	main()
"""
black, white = getPlayers()
board, score = play(black, white)
