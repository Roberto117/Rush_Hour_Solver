
from io import open
from Car import Car, MAX_CAR_SIZE , MIN_CAR_SIZE
from Orientation import Orientation
import sys
from copy import deepcopy
class Board():
	width  = 0 #the width of the board
	height = 0 #the height of the board
	exit_pos = [-1 , -1] #x ,y coordinates pointing to the exit 
	cars   = {}
	HORIZONTAL_VALID_MOVES = ["L", "R"] #The valid inputs for a horizontal car
	VERTICAL_VALID_MOVES = ["U","D",]#The valid moves for a vertical car
	player_car_label = "@"#The default label for the car that needs to reach the exit
	
	def __init__(self, init):
		#The Board function has two ways to be initilized
		#By a text file that contains the starting configurations
		#By copying another Board Object
		if isinstance( init , str):
			self.loadLevelFromFile(init)
		else:
			self.width = init.width
			self.height = init.height
			self.exit_pos = init.exit_pos
			#The cars dictionary needs to be deepcopied so that the Car Objects are inmutable
			self.cars =  deepcopy(init.cars)


	def getBoard(self):
		#create an emoty board
		board = [[] for row in range(self.height)]
		for row in range(self.height):
			for tile in range(self.width):
				#add a tile to the board if is a border tile then + else -
				if row in [0,self.height -1] or tile in [0 , self.width -1 ]:
					board[row].append("+")
				else:
					board[row].append("-")

		board[self.exit_pos[1]][self.exit_pos[0]] = "#"#add the exit tile
		for label, car in self.cars.items():
			#iterate through every car an add them to the board
			start_pos = car.initial_x if car.isHorizontal() else car.initial_y
			for pos in range(start_pos, start_pos + car.size):
				if car.isHorizontal():
					#add the car's label for each tile they are at
					board[car.initial_y][pos] =  car.label
				else:
					board[pos][car.initial_x] =  car.label
		board_string = ""
		#loop through the board to create the board string
		for row in board:
			for tile in row:
				board_string += tile + " "
			board_string += "\n"
		return board_string

	def loadLevelFromFile(self, level_file):
		#this function will take a file path to a text file and convert it to an intial configuration
		file = open(level_file, "r")
		#split the string given into a list of string for every new line
		draft_board= file.read().splitlines()
		file.close()

		for rowIndex, row in enumerate(draft_board):
			if rowIndex == 0:
				self.width = len(row)#set the boards width
				self.height = len(draft_board)# set the boards heigh
			
			elif self.width != len(row):
				#exit if the board is disproportionate
				print("not all rows have the same size")
				sys.exit(0)

			for tileIndex, tile in enumerate(row):
				if tile == "#":
					#if the tile is # this is the exit tile and we store in the Board Object
					self.exit_pos = [tileIndex,rowIndex]
				elif tile not in ["-", "+"] and tile not in self.cars:
					#if the tile is anything other than - +, then it is a car tile so we add it tot he car dictionary
					draft_board=  foundCar(draft_board, tile, tileIndex, rowIndex, self.cars)
		
		if self.exit_pos[0] == -1:
			#if no # is found then the board given is invalid, so we exit
			print("No exit found")
			sys.exit(0)
		if self.player_car_label not in self.cars:
			#if no @ is found then there is no red car so the board is invalid and we exit
			print("Red car not found")
			sys.exit(0)

	def moveCar(self, move_command):
		#We check if the input given is valid if yes we move the car
		if len(move_command) > 3:
			#if the string given is bigger than 3 chars is invalid
			print("Inpout is too large! only use two characters \n one for the car label and one for the direction\n for example AU to move the A car Up one unit")
			return False
		move_command = move_command.upper()
		label = move_command[0] # the car label
		move = move_command[1] #the move direction
		amount = move_command[2]#the amount to move
		if label not in self.cars:
			#if the car does not exit the input is invalid
			print("The car label does not exist on the board, try again")
			return False
		if self.cars[label].isHorizontal() and move not in self.HORIZONTAL_VALID_MOVES:
			#if the car is horizontal and the direction given is not left or right, the input is invalid
			print("Second Character is not a valid move for car:%s please use the following:" %label)
			print("L: Move LEFT one cell") 
			print("R: Move RIGHT one cell")
			return False
		elif self.cars[label].isVertical() and move not in self.VERTICAL_VALID_MOVES:
			#if the car is vertical and the directions is not up or down, the input is invalid
			print("Second Character is not a valid move for car:%s please use the following:" %label)
			print("U: Move UP one cell") 
			print("D: Move DOWN one cell")
			return False
		if not amount.isdigit():
			#if the last char is not a digit the input is invalid
			print("Third Charactes is not a valid integer")
			return False

		if (self.cars[label].isVertical() and move == "U") or (self.cars[label].isHorizontal() and move == "L"):
			#if the direction that the car will go is a negative direction we invert the ammount to move
			amount = int(amount) * -1
		else:
			amount = int(amount)

		return self.tryMove(label,amount) #return true if moved succesfully otherwise return false

	def tryMove(self, label,amount):
		#We try to move a car with the given input
		car = self.cars[label]

		#Check if moving the car puts it out of the game area
		if car.isHorizontal():
			if car.initial_x + amount <= 0 or (car.initial_x + car.size -1 )+ amount >= self.width -1:
				print("Move is out of bounds, try again!")
				return False
		else:
			if car.initial_y + amount <= 0 or (car.initial_y + car.size -1 ) + amount >= self.height -1:
				print("Move is out of bounds, try again!") 
				return False

		for car_label in self.cars:
			#Check for collision against all cars
			if self.cars[car_label].label != label and car.checkCollision(self.cars[car_label], amount):
				print("Collision Detected with car:%s! \n try again" %self.cars[car_label].label)
				return False #if there was collision we return false and we do not modify the car
		
		if car.isHorizontal():
			#if there was no collision detected we updated the car to its ned position
			car.initial_x += amount 
		else:
			car.initial_y += amount
		return True


	def sudoMoveCar(self, move_command):
		#simlar to the moveCar function except there is not print functions
		#and the function returns the Board Object if its a valid move otherwise it returns None
		#this function is used when solving the puzzle
		if len(move_command) > 3:
			return None
		move_command = move_command.upper()
		label = move_command[0]
		move = move_command[1]
		amount = move_command[2]
		if label not in self.cars:
			return None
		if self.cars[label].isHorizontal() and move not in self.HORIZONTAL_VALID_MOVES:
			return None
		elif self.cars[label].isVertical() and move not in self.VERTICAL_VALID_MOVES:
			return None
		if not amount.isdigit():
			return None

		if (self.cars[label].isVertical() and move == "U") or (self.cars[label].isHorizontal() and move == "L"):
			amount = int(amount) * -1
		else:
			amount = int(amount)

		return self if self.sudoTryMove(label,amount) else None

	def sudoTryMove(self, label,amount):
		#similar to the tryMove function but without print statments
		#this function is used when solving the puzzle
		car = self.cars[label]
		if car.isHorizontal():
			if car.initial_x + amount <= 0 or (car.initial_x + car.size -1 )+ amount >= self.width -1:
				return False
		else:
			if car.initial_y + amount <= 0 or (car.initial_y + car.size -1 ) + amount >= self.height -1:
				return False

		for car_label in self.cars:
			if self.cars[car_label].label != label and car.checkCollision(self.cars[car_label], amount):
				return False
		
		if car.isHorizontal():
			car.initial_x += amount 
		else:
			car.initial_y += amount
		return True

	def checkIfWin(self):
		#Check if the red car's x2 coordinate is one off from the exit tile if yes, return true, false otherwise
		player_coord = self.cars[self.player_car_label].getCoordinates()
		if self.cars[self.player_car_label].isHorizontal():
			return player_coord.x2 +1 ==self.exit_pos[0]
		else:
			return player_coord.y2 +1 == self.exit_pos[1]


def foundCar(board,car_label, initial_x, initial_y , cars_dict):
	#this funtion will add a Car to the given car dictionary

	size = 0#size of the car
	#check the orientation of the car by checking what adjacent coordinate has the same car label
	#depending of what axis we move on this will tell us the coordinates, for example if the next car label is
	#on the [original x +1, original y] then the car is horizontal  
	orientation = Orientation.HORIZONTAL if board[initial_y][initial_x+1] == car_label else Orientation.VERTICAL

	start_pos = initial_x  if orientation == Orientation.HORIZONTAL else initial_y
	for start_pos in range(start_pos, start_pos + MAX_CAR_SIZE):
		#find all car labels change them to empty tiles and store it in the car dictionary
		if orientation == Orientation.HORIZONTAL:
			#add one to the size if the car label is found
			if board[initial_y][start_pos] != car_label:
				break;
			else:
				size += 1 
		else:
			if board[start_pos][initial_x] != car_label:
				break;
			else:
				size += 1#
	if size < MIN_CAR_SIZE:
		#if the car is to small, the board is invalid and we exit
		print("car at start pos (%s,%s) is too small" %(str(initial_x), str(initial_y)))
		sys.exit(0)
	#add the new found car to the dictionary
	cars_dict[car_label] = Car(car_label,initial_x, initial_y , size , orientation)

	#cars_dict[car_label].printCar()
	return board