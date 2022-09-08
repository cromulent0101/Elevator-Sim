# pylint: disable=import-error
from classes import Elevator, Rider, Floor
import utils
from time import sleep
from sys import maxsize
import random

# rider_list = utils.get_riders()
rider_list = [
    Rider("Joe", 2, 9),
    Rider("Bob", 5, 9),
    Rider("Jane", 1, 9),
    Rider("John", 12, 9),
    Rider("poop", 12, 9),
]

# create an elevator at a random floor
e = Elevator(3, 3)

floor_dict = utils.create_floors(rider_list)

# arbitrarily choose elevator to go up first
e.direction = 1

output = e.run(rider_list, floor_dict)
print(output)
