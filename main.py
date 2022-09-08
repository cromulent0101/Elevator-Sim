# pylint: disable=import-error
from classes import Elevator, Rider, Floor
import utils
from time import sleep
from sys import maxsize
import random

# rider_list = utils.get_riders()
rider_list = [
    Rider("Joe", 2, 9),
    Rider("Bob", 2, 5),
    Rider("Jane", 3, 5),
    Rider("Jimmy", 5, 9),
    Rider("Jill", 9, 5),
]

# create an elevator at a random floor
e = Elevator(3, 12)
e_bank = [e]

floor_dict = utils.create_floors(rider_list, e_bank)

# arbitrarily choose elevator to go up first
e.direction = -1

output = e.run(rider_list, floor_dict)
print(output)
