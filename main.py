# pylint: disable=import-error
import utils
import csv
import random
import os
from classes import Elevator, Rider, Floor, ElevatorBank
from statistics import mean, median

SIMULATION_CSV = "sims/classic.csv"
ELEVATOR_CAPACITY = 3
NUM_ELEVATORS = 2
TIME_STEP = 0.01
MAX_TIME = 10000

rider_list_csv = utils.get_riders_from_csv(SIMULATION_CSV)
rider_list_csv_floor = utils.get_riders_from_csv(SIMULATION_CSV)


a = Elevator(ELEVATOR_CAPACITY, 1, "a")
b = Elevator(ELEVATOR_CAPACITY, 3, "b")
c = Elevator(ELEVATOR_CAPACITY, 1, "c")
d = Elevator(ELEVATOR_CAPACITY, 1, "d")
e = Elevator(ELEVATOR_CAPACITY, 1, "e")
f = Elevator(ELEVATOR_CAPACITY, 1, "f")
a_floor = Elevator(ELEVATOR_CAPACITY, 1, "a_floor")
b_floor = Elevator(ELEVATOR_CAPACITY, 1, "b_floor")
c_floor = Elevator(ELEVATOR_CAPACITY, 1, "c_floor")
d_floor = Elevator(ELEVATOR_CAPACITY, 1, "d_floor")
e_floor = Elevator(ELEVATOR_CAPACITY, 1, "e_floor")
f_floor = Elevator(ELEVATOR_CAPACITY, 1, "f_floor")

e_bank = [a, b, c, d, e, f]
e_bank_floor = [a_floor, b_floor, c_floor, d_floor, e_floor, f_floor]


bank = ElevatorBank(e_bank[:NUM_ELEVATORS])
bank_floor = ElevatorBank(e_bank_floor[:NUM_ELEVATORS])
floor_dict = utils.create_floors(rider_list_csv, e_bank[:NUM_ELEVATORS])
floor_dict_floor = utils.create_floors(
    rider_list_csv_floor, e_bank_floor[:NUM_ELEVATORS]
)

if __name__ == "__main__":

    start_step_delays, start_stop_delays, floors_traversed, log_dict = bank.simulate(
        rider_list_csv, floor_dict, TIME_STEP, MAX_TIME, "elevate"
    )

    (
        start_step_delays_floor,
        start_stop_delays_floor,
        floors_traversed_floor,
        log_dict_floor,
    ) = bank_floor.simulate(
        rider_list_csv_floor, floor_dict_floor, TIME_STEP, MAX_TIME, "elevate_dc"
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

    # utils.test_helper(log_dict)
