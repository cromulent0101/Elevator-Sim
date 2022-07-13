# pylint: disable=import-error
from classes import InefficientElevator, Rider, Floor
import utils
from time import sleep
from sys import maxsize
import random

# rider_list = utils.get_riders()
rider_list = [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 1, 9)]

# create an elevator at a random floor
e = InefficientElevator(3, 3)

# create Floors and populate with Riders
min_start_floor = min([rider.start_floor for rider in rider_list])
min_destination = min([rider.destination for rider in rider_list])
max_start_floor = max([rider.start_floor for rider in rider_list])
max_destination = max([rider.destination for rider in rider_list])
min_floor = min([min_start_floor, min_destination])
max_floor = max([max_start_floor, max_destination])

floor_dict = {}
# populate dict of floors with each floor traversable and press up or down buttons on those floors
for floor_num in range(min_floor - 1, max_floor + 2):
    floor_dict[floor_num] = Floor(floor_num)
    for rider in rider_list:
        if rider.start_floor == floor_num:
            floor_dict[floor_num].riders.append(rider)
            if rider.start_floor > rider.destination:
                floor_dict[floor_num].down_request = True
            else:
                floor_dict[floor_num].up_request = True

# arbitrarily choose elevator to go up first
e.direction = 1
floors = floor_dict.values()
# keep_going_up = any(floor.up_request for floor in floors)


place = e.run(rider_list, floor_dict)
print(place)
