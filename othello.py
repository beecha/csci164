import random #For randomizing AI's legal actions
import sys


""" --------------- Defining Symbols and Directions --------------------
"""
#Symbols to be use on the game board
EMPTY = ''
BLACK = 'O'
WHITE = 'X'
EDGES = '.'
PIECES = (EMPTY, BLACK, WHITE, EDGES)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}


#Defining the moves and directions sets
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
"""------------------------------------------------------------------"""




"""------------ Define & Initialize The Game Board----------------------
"""
#Allocate the range of the board
def squares():
	return (i for i in xrange(11, 89) if i <= (i % 10) <= 8)
	
	
#Initialize the starting pieces of the board
def initial_board():
	board = [EDGES] * 100
	for i in squares():
		board[i] = EMPTY
	
	board[44], board[45] = WHITE, BLACK
	board[54], board[55] = BLACK, WHITE
	
	return board
	
	
def display_board(board):
	rep = ' '
	rep += ' %s\n' % ' '.join(map(str, range(1, 9) ) )
	for row in xrange(1, 9):
		begin, end = 10 * row + 1, 10 * row + 9
		rep += '%d %s\n' % (row, ' '.join(board[begin:end]) )
	return rep



"""
------------------ Checking For Valid & Legal Actions ------------------
The rules for moving onto a block square is that it has
to be an empty block. But in order to be able to place
your block on the square, an opponent piece has to be
adjacent to the square block in all DIRECTIONS
"""
#Check if the current square block is a valid square to move onto
def isValid(move):
	return isInstance(move, int) and move in squares()
	
#Get the "Symbol" of the player making the move
def opponent(player):
	return BLACK if player is WHITE else WHITE
	
#Check if the adjacent square block is the opponent's symbol
#If it's your own symbol, return none and it's not a
#valid square block to move on to
def findBracket(square, player, board, direction):
	bracket = square + direction
	if board[bracket] == player:
		return None
	opp = opponent
	while board[bracket] == opp:
		bracket += direction
	return None if board[bracket] in (OUTER, EMPTY) else bracket

#Legalize the action to move
def isLegal(move, player, board):
	hasBracket = lambda direction : findBracket(move, player, board, direction)
	return board[move] == EMPTY and any(map(hasBracket, DIRECTIONS) )
"""------------------------------------------------------------------"""





"""--------------------- Flipping The Bracket Pieces -------------------
"""
def makeMove(move, player, board):
	board[move] = player
	for d in DIRECTIONS:
		makeFlips(move, player, board, d)
	return board
	

def makeFlips(move, player, board, direction):
	bracket = findBracket(move, player, board, direction)
	if not bracket:
		return
	square = move + direction
	while square != bracket:
		board[square] = player
		square += direction
"""------------------------------------------------------------------"""



"""--------------Throw An Error for Illegal Moves-----------------------
If the player tries to place a game piece on an invalid block, then it
will get an error. So it'll be easier if all the legal moves are already
given to the player.
"""
class IllegalMoveError(Exception):
	def __init__(self, player, move, board):
		self.player = player
		self.move = move
		self.board = board
	def __str__(self):
		return '%s Cannot Move To Square %d' % (PLAYERS[self.player], self.move)

def legalMoves(player, board):
	return [sq for sq in squares() if isLegal(sq, player, board) ]
	
def anyLegalMove(player, board):
	return any(isLegal(sq, player, board) for sq in squares() )
"""------------------------------------------------------------------"""



"""------------------------Moving The Pieces---------------------------- 
"""
def play(black_approach, white_approach):
	board = initial_board()
	player = BLACK
	approach = lambda who: black_approach if who == BLACK else white_approach
	while player is not None:
		move = getMove(approach(player), player, board)
		makeMove(move, player, board)
		player = nextPlayer(board, player)
	return board, score(BLACK, board)
	
#There's a possibility of having NO LEGAL MOVES given to a player
#If that's the case, the player will skip its turn
def nextPlayer(board, previousPlayer):
	opp = opponent(previousPlayer)
	if anyLegalMove(opp, board):
		return opp
	elif anyLegalMove(previousPlayer, board):
		return previousPlayer
	return None


def getMove(approach, player, board):
	copy = list(board)
	move = approach(player, copy)
	if not isValid(move) or not isLegal(move, player, board):
		raise IllegalMoveError(player, move, copy)
	return move
"""------------------------------------------------------------------"""





"""-----------------Scoring Both Player's Points------------------------
"""
#Loop through each square block and add the number of pieces
#accordingly to the player or the opponent's symbol
def playerScore(player, board):
	p1, p2 = 0, 0
	opp = opponent(player)
	for sq in squares():
		piece = board[sq]
		if piece == player:
			p1 += 1
		elif piece == opp:
			p2 += 1
	return p1 - p2
"""------------------------------------------------------------------"""


"""------------------Approach for AI Play Style-------------------------
"""
#The AI will choose any random legal moves available to it
def randomApproach(player, board):
	return random.choice(legalMoves(player, board) )




