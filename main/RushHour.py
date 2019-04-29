from Board import *
from Solver import *
import random


def printHelp():
	print("To move a car you need to write 3 characters\nthe car label for example A, \ndirection [U = UP, D = DOWN, L = LEFT, R = RIGHT ]\nand the amount of move for example 2\nif you would like for the game to be solved type SOLVE ")
if __name__ == "__main__":
	#ask the user to input the difficulty
	#there is a total of 40 levesl 10 levels per difficulty scale
	difficulty_input = input("Choose difficulty \n 1: easy \n 2: medium \n 3: hard \n 4: expert \n") 
	while(not difficulty_input.isdigit() and difficulty_input < 1 and  difficulty_input > 4):
		difficulty_input = input("Choose difficulty \n 1: easy \n 2: medium \n 3: hard \n 4: expert")

	if difficulty_input == "1":
		difficulty = "easy"
	elif difficulty_input == "2":
		difficulty = "medium"
	elif difficulty_input == "3":
		difficulty = "hard"
	else:
		difficulty = "expert"
	#choose a random level based on the difficulty
	level_title =  str(random.randint(1,10))
	level = "levels/%s/level%s" % ( difficulty , level_title)
	#load the level 
	board = Board(level)

	#print instructions
	printHelp()
	while( not board.checkIfWin()):
		#print the board
		print("Level %s" %level_title)
		print(board.getBoard())
		#ask for user input
		i = input("Type a move command or type HELP for instructions:")
		#check for speacial cases
		if i.upper() == "HELP":
			printHelp()
		elif i.upper() == "SOLVE":
			print("Solving.....")
			#try to solve
			solution = solve(board)
			#print the solution
			optimized_move_set =  optimizeMoveSet(solution.moves)
			print("Solved! in %s moves" %len(optimized_move_set))
			for move in optimized_move_set:
				print(move)
				board.moveCar(move)
				print(board.getBoard())
		else:
			#move a car bases on user input
			board.moveCar(i)

	print(board.getBoard())
	print("You Win!")