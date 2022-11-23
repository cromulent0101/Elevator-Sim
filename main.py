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


rider_list_csv = utils.get_riders_from_csv("sims/100random.csv")

e = Elevator(100, 80)
t = Elevator(100, 3)
stationary = Elevator(3, 3)
e.direction = -1
t.direction = 1
stationary.direction = 0

e_bank = [e, t]
bank = ElevatorBank(e_bank)

start_stop_delays = []
start_step_delays = []

floor_dict = utils.create_floors(rider_list_csv, e_bank, bank)

start_step_delays, start_stop_delays, log_dict = bank.simulate(
    rider_list_csv, floor_dict
)


print(f"Average total wait: {mean(start_stop_delays)}")
print(f"Median total wait: {median(start_stop_delays)}")
print(f"Average floor wait: {mean(start_step_delays)}")
print(f"Median floor wait : {median(start_step_delays)}")
print(log_dict)
