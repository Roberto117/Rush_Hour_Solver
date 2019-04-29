from Board import *
from Car import *
from collections import *
from copy import copy

#structure to a store a single possible configuration
Configuration = namedtuple("Moves", ['board', 'moves'])

def solve(board):
	return bfs([Configuration(board, [])], {board.getBoard()}, 500)


def bfs(configurations , past_boards ,steps_left ):
	#to solve the game I take a breath first search aproach
	#this function takes in three items, a list of possible configurations
	#a dictionary of past board configurations
	#and the number of steps allowed
	if steps_left > 0:
		next_configs = []
		for config in configurations:
			for car in config.board.cars:
				for direction in ["U","D","L","R"]:
					#for each car in the current configuratins we will create at most 2 board
					#one for each possible move (a car con at most move in two different directions at onces)
					newboard = Board(config.board)
					move_command = car+direction+"1"
					#we try to move the car the if a board is returned then the move was succesfull
					newboard  = newboard.sudoMoveCar(move_command)
					if newboard:
						board_string = newboard.getBoard()
						if board_string not in past_boards:
							#we check if the board has been seen before in any previous configurations
							#if not we append it to the dictionary
							#we create a new move possible congiguration (this one)
							past_boards.add(board_string)
							prev_moves = copy(config.moves)
							prev_moves.append(move_command)
							new_config = Configuration(newboard, prev_moves)
							
							if newboard.checkIfWin():
								#we check if this configuration wins the game
								#if yes we exit and return this configuration
								#if not we append this configuration to the configurtaions list
								#and continue searching
								return new_config
							else:
								next_configs.append(new_config)
		return bfs(next_configs, past_boards, steps_left -1)#go down one level
	return None


def optimizeMoveSet(moves):
	#because the solver will move each car only by one block each loop through the function
	#there are times where a move set can be for example ["AU1", "AU1", "AU1", "BD1", "BD1", "@R1", "@R1"]
	#while this is a valid move set it can be shortened to ["AU3", "BD2", "@R2" ]
	#this function tries to convert it to that shortened list so that the user can see the shortest move set possible
	new_move_set = []
	prev_move = ""
	move_command = ""
	for move in moves:
		if prev_move ==  move:
			#if the next move is the same as the previous one that means it can be shortened
			move_command = move_command[:2] + str( int(move_command[2]) +1 )
		else:
			#if this is a new move command then the previous one can not be shortened so we update
			if move_command != "":
				new_move_set.append(move_command)
			move_command =  move
		prev_move = move 
	new_move_set.append(move_command)
	return new_move_set