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


rider_list_csv = utils.get_riders_from_csv("sims/office.csv")

e = Elevator(100, 80)
t = Elevator(100, 3)
z = Elevator(100, 1)
q = Elevator(100, 60)

e.direction = 0
t.direction = 0
z.direction = 0
q.direction = 0

e_bank = [t, z]
bank = ElevatorBank(e_bank)
floor_dict = utils.create_floors(rider_list_csv, e_bank, bank)

start_step_delays, start_stop_delays, log_dict = bank.simulate(
    rider_list_csv, floor_dict
)

print(f"Overall total wait: {sum(start_stop_delays)}")
print(f"Floor total wait: {sum(start_step_delays)}")
print(f"Average total wait: {mean(start_stop_delays)}")
print(f"Median total wait: {median(start_stop_delays)}")
print(f"Average floor wait: {mean(start_step_delays)}")
print(f"Median floor wait : {median(start_step_delays)}")
print(log_dict)
