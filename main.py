# TODO: add main dunder
# pylint: disable=import-error
from classes import Elevator, Rider, Floor
import utils
import csv
from time import sleep
from sys import maxsize
from statistics import mean, median
import random
import threading
import concurrent.futures
import tkinter as tk


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
t = Elevator(3, 12)
e_bank = [e]

start_stop_delays = []
start_step_delays = []

floor_dict = utils.create_floors(rider_list, e_bank)

# arbitrarily choose elevator to go up first
e.direction = -1
t.direction = 1

el1 = Elevator(3, 10)
el1.direction = -1
el2 = Elevator(3, 6)
el2.direction = -1
el3 = Elevator(3, 4)
el3.direction = 0
el4 = Elevator(3, 4)
el4.direction = -1
el5 = Elevator(3, 1)
el5.direction = 1
elevator_bank = [el1, el2, el3, el4, el5]

print(utils.find_nearest_available_elevator(Rider("Joe", 2, 5), elevator_bank))

e.elevate(rider_list, floor_dict, start_stop_delays, start_step_delays)
# t1 = threading.Thread(
#     target=e.elevate,
#     args=[rider_list, floor_dict, start_stop_delays, start_step_delays],
# )
# t2 = threading.Thread(target=utils.update_riders, args=[rider_list, floor_dict])

# t1.start()
# sleep(2)
# # t2.start()
# t1.join()
# # t2.join()
# # output = e.elevate(rider_list, floor_dict)
# # print(output)

print(f"Average total wait: {mean(start_stop_delays)}")
print(f"Median total wait: {median(start_stop_delays)}")
print(f"Average floor wait: {mean(start_step_delays)}")
print(f"Median floor wait: {median(start_step_delays)}")
