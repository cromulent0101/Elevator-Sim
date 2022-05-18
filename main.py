# pylint: disable=import-error
from classes import InefficientElevator, Rider
import utils
from time import sleep
from sys import maxsize
import random

# rider_list = utils.get_riders()
rider_list = [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 1, 9)]
# create an elevator at a random floor
e = InefficientElevator(3, 4)


# to begin, all riders call an elevator to their start_floor at once
# this gotta change once I add more than one elevator
for rider in rider_list:
    e.destinations.add(rider.start_floor)

# arbitrarily choose elevator to go up first
e.direction = 1

place = e.run(rider_list)
print(place)
