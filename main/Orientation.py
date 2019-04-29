from enum import Enum, unique, auto
@unique
class Orientation(Enum):
	#this is an enumerator class to keep track on a cars orientation in the board
	HORIZONTAL = auto()
	VERTICAL = auto()