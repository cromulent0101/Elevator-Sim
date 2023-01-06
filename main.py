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


simluation_csv = "sims/classic.csv"
rider_list_csv = utils.get_riders_from_csv(simluation_csv)
rider_list_csv_floor = utils.get_riders_from_csv(simluation_csv)

elevator_capacity = 1
num_elevators = 3

a = Elevator(elevator_capacity, 1, "a")
b = Elevator(elevator_capacity, 1, "b")
c = Elevator(elevator_capacity, 1, "c")
d = Elevator(elevator_capacity, 1, "d")
e = Elevator(elevator_capacity, 1, "e")
f = Elevator(elevator_capacity, 1, "f")
a_floor = Elevator(elevator_capacity, 1, "a_floor")
b_floor = Elevator(elevator_capacity, 1, "b_floor")
c_floor = Elevator(elevator_capacity, 1, "c_floor")
d_floor = Elevator(elevator_capacity, 1, "d_floor")
e_floor = Elevator(elevator_capacity, 1, "e_floor")
f_floor = Elevator(elevator_capacity, 1, "f_floor")

e_bank = [a, b, c, d, e, f]
e_bank_floor = [a_floor, b_floor, c_floor, d_floor, e_floor, f_floor]


bank = ElevatorBank(e_bank[:num_elevators])
bank_floor = ElevatorBank(e_bank_floor[:num_elevators])
floor_dict = utils.create_floors(rider_list_csv, e_bank[:num_elevators])
floor_dict_floor = utils.create_floors(
    rider_list_csv_floor, e_bank_floor[:num_elevators]
)

time_step = 0.01
max_time = 10000

start_step_delays, start_stop_delays, floors_traversed, log_dict = bank.simulate(
    rider_list_csv, floor_dict, time_step, max_time, "elevate"
)

(
    start_step_delays_floor,
    start_stop_delays_floor,
    floors_traversed_floor,
    log_dict_floor,
) = bank_floor.simulate(
    rider_list_csv_floor, floor_dict_floor, time_step, max_time, "elevate_floor"
)


print(log_dict_floor)
print(log_dict)
print(f"Overall total wait: {sum(start_stop_delays)}")
print(f"Overall total wait dispatch: {sum(start_stop_delays_floor)}")
print("")
print(f"Floor total wait: {sum(start_step_delays)}")
print(f"Floor total wait dispatch: {sum(start_step_delays_floor)}")
print("")
print(f"Average total wait: {mean(start_stop_delays)}")
print(f"Average total wait dispatch: {mean(start_stop_delays_floor)}")
print("")
print(f"Median total wait: {median(start_stop_delays)}")
print(f"Median total wait dispatch: {median(start_stop_delays_floor)}")
print("")
print(f"Average floor wait: {mean(start_step_delays)}")
print(f"Average floor wait dispatch: {mean(start_step_delays_floor)}")
print("")
print(f"Median floor wait: {median(start_step_delays)}")
print(f"Median floor wait dispatch: {median(start_step_delays_floor)}")
print("")
print(f"Floors traversed: {floors_traversed}")
print(f"Floors traversed by dispatch: {floors_traversed_floor}")
