# pylint: disable=import-error
from classes import Elevator, Rider
from time import sleep
from sys import maxsize
import random


print(rider_list[0])
# create an elevator at a random valid floor
e = Elevator(3, random.randint(lowest_rider_floor, highest_rider_floor))


# to begin, all riders call an elevator to their start_floor at once
# this gotta change once I add more than one elevator
for rider in rider_list:
    e.destinations.add(rider.start_floor)

# arbitrarily choose elevator to go up first
e.direction = 1

place = e.run(rider_list)
print(place)
