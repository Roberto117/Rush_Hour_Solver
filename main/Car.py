from Orientation import Orientation
import collections

#Structure to keep the coordinates of a car
Coordinates = collections.namedtuple('Coordinates', ['x1', 'x2', 'y1', 'y2'])
MAX_CAR_SIZE = 3#the biggest size a car can be
MIN_CAR_SIZE = 2#the minumum size a car can be
class Car():
	initial_x = 0 #the first x position
	initial_y = 0#the first y position
	label = ''#the car's label
	size = 0#how many blocks the car takes
	orientation =  Orientation.HORIZONTAL#the orientation of the car
	def __init__(self, car_label, initial_x, intial_y , size , orientation):
		self.initial_x = initial_x
		self.initial_y = intial_y 
		self.size = size
		self.orientation =  orientation
		self.label =  car_label

	def isHorizontal(self): return self.orientation == Orientation.HORIZONTAL

	def isVertical(self): return self.orientation == Orientation.VERTICAL

	def printCar(self):
		#prints the cars items
		#mostly used for debbuging
		print("orientation:%s" % self.orientation)
		print("initial_x:%s" %str(self.initial_x))
		print("initial_y:%s"%str(self.initial_y))
		print("label%s" % self.label)
		print("size:%s"% str(self.size))
	
	def getCoordinates(self):
		#return the x y coordinates of the car
		return Coordinates(self.initial_x, self.initial_x + self.size -1, self.initial_y, self.initial_y) if self.isHorizontal() else Coordinates(self.initial_x, self.initial_x, self.initial_y, self.initial_y + self.size -1)

	def checkCollision(self, car2 , amount):
		#check if this car collides with the given car
		#this function assumes the car has not move yet and
		#insted the amount the car is to be moved is given
		coord1 = self.getCoordinates()
		coord2 = car2.getCoordinates()

		#for collision check we do a simple Bounding Box collision check with a small modification
		#the difference being that one of the coordinates will expand based on the amount given and the orientation of the car
		#for example if the car is horizontal and the amount is negative then the x1 diretion will expand so that the car expands left
		#this will simulate all the blocks the car will pass through to get to that position and then we can do a bouding box check
		if self.isHorizontal():

			if amount >= 0:
				return (coord1.x1 <= coord2.x2  and coord1.x2 + amount >= coord2.x1 and coord1.y1 <= coord2.y2 and coord1.y2  >= coord2.y1)
			else:
				return (coord1.x1 + amount  <= coord2.x2  and coord1.x2 >= coord2.x1  and coord1.y1 <= coord2.y2 and coord1.y2  >= coord2.y1)
		else:
			if amount >= 0:
				return (coord1.x1 <= coord2.x2 and coord1.x2 >= coord2.x1 and coord1.y1  <= coord2.y2  and coord1.y2 + amount  >= coord2.y1 )
			else:
				return (coord1.x1  <= coord2.x2 and coord1.x2 >= coord2.x1 and coord1.y1 + amount <= coord2.y2 and coord1.y2  >= coord2.y1 )
			