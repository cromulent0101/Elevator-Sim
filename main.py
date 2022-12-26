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


rider_list_csv = utils.get_riders_from_csv("sims/edge_cases.csv")
rider_list_csv_floor = utils.get_riders_from_csv("sims/edge_cases.csv")

t = Elevator(1, 3, "t")
z = Elevator(1, 1, "z")
t_floor = Elevator(1, 3, "t_floor")
z_floor = Elevator(1, 1, "z_floor")

e_bank = [t, z]
e_bank_floor = [t_floor, z_floor]

bank = ElevatorBank(e_bank)
bank_floor = ElevatorBank(e_bank_floor)
floor_dict = utils.create_floors(rider_list_csv, e_bank)
floor_dict_floor = utils.create_floors(rider_list_csv_floor, e_bank_floor)

time_step = 0.01
max_time = 10000


start_step_delays, start_stop_delays, log_dict = bank.simulate(
    rider_list_csv, floor_dict, time_step, max_time
)

(
    start_step_delays_floor,
    start_stop_delays_floor,
    log_dict_floor,
) = bank_floor.simulate_floor(
    rider_list_csv_floor, floor_dict_floor, time_step, max_time
)


print(f"Overall total wait: {sum(start_stop_delays)}")
print(f"Floor total wait: {sum(start_step_delays)}")
print(f"Average total wait: {mean(start_stop_delays)}")
print(f"Median total wait: {median(start_stop_delays)}")
print(f"Average floor wait: {mean(start_step_delays)}")
print(f"Median floor wait : {median(start_step_delays)}")
print(log_dict_floor)
print(log_dict)
