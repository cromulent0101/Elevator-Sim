# TODO: add main dunder
# pylint: disable=import-error
from classes import Elevator, Rider, Floor, ElevatorBank
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
# rider_list = [
#     Rider("Joe", 2, 9),
#     Rider("Bob", 2, 5),
#     Rider("Jane", 3, 5),
#     Rider("Jimmy", 5, 9),
#     Rider("Jill", 9, 5),
# ]
rider_list = utils.get_riders_from_csv("sims/sim1.csv")
# create an elevator at a random floor
e = Elevator(3, 12)
t = Elevator(3, 3)
e.direction = 0
t.direction = 1

e_bank = [e]
bank = ElevatorBank(e_bank)

start_stop_delays = []
start_step_delays = []

floor_dict = utils.create_floors(rider_list, e_bank)

# arbitrarily choose elevator to go up first

bank.simulate(rider_list, floor_dict)
# e.elevate(rider_list, floor_dict, start_stop_delays, start_step_delays)
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
