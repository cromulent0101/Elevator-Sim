from dataclasses import dataclass
from time import sleep, time
from sys import maxsize
from queue import Queue
import csv
from typing import Set
import tkinter as tk
import threading
import logging

active_riders = []  # make a Queue?


def rider_update(rider_list, floor_dict, e_bank):
    floor_dict["done"] = False
    while rider_list:
        for rider in rider_list:
            if (
                rider.when_to_add < (time() - e_bank.begin_time)
                and not rider.button_pressed
            ):
                rider.press_button(floor_dict)
                active_riders.append(rider)
                rider_list.remove(rider)
        sleep(1)
    while active_riders:
        sleep(1)
    floor_dict["done"] = True


class ElevatorBank:
    def __init__(self, e_bank):
        self.elevators = e_bank
        self.queue = Queue()  # floors that don't have an elevator going to them yet
        self.begin_time = time()

    def simulate(self, rider_list_csv: list, floor_dict: dict):
        threads = []
        start_stop_delays = []
        start_step_delays = []
        log_dict = {}
        rider_updater = threading.Thread(
            target=rider_update,
            args=[rider_list_csv, floor_dict, self],
            name="Rider Updater",
        )
        rider_updater.start()
        threads.append(rider_updater)
        for idx, e in enumerate(self.elevators, start=1):
            log_dict[f"Elevator {idx}"] = []
            t1 = threading.Thread(
                target=e.elevate,
                args=[
                    rider_list_csv,
                    floor_dict,
                    start_stop_delays,
                    start_step_delays,
                    self,
                    log_dict,
                ],
                name=f"Elevator {idx}",
            )
            t1.start()
            threads.append(t1)
        for t in threads:
            t.join()
        return start_step_delays, start_stop_delays, log_dict


class Elevator:
    def __init__(self, capacity: int, floor):
        self.floor = floor
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.internal_destinations = set()  # Set of ints. Can we type this?
        self.external_destinations = set()
        self.door_delay = 1
        self.elevator_delay = 0.5
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did

    def __eq__(
        self, other
    ):  # FYI implementing this makes Elevators not be able to be in sets/dicts
        if not isinstance(other, Elevator):
            return NotImplemented

        return self.floor == other.floor and self.direction == other.direction

    def __str__(self):
        return f"{self.floor}  {self.direction}"

    def __repr__(self):
        return f"Elevator is on {self.floor} and direction {self.direction}"

    def elevate(
        self,
        rider_list,
        floor_dict,
        start_stop_delays,
        start_step_delays,
        e_bank,
        log_dict,
    ):
        """
        Tells an elevator to pick up and drop off passengers
        given a rider list.

        Returns a string that represents the actions taken by
        the elevator.
        """
        while not floor_dict["done"]:
            for rider in self.riders:
                rider.curr_floor = self.floor

            door_open_out, rider_names_to_remove = self.let_riders_out(
                active_riders,
                start_stop_delays,
                start_step_delays,
            )
            self.update_direction(floor_dict)
            door_open_in, rider_names_to_add = self.let_riders_in(floor_dict)
            self.log = self.log_movement(
                rider_names_to_add, rider_names_to_remove, log_dict
            )
            self.floor += self.direction
            self.simulate_delays(door_open_in, door_open_out)
            print(self.log)

    def simulate_delays(self, door_open_in, door_open_out):
        if door_open_in or door_open_out:
            sleep(self.door_delay)
        sleep(self.elevator_delay)

    def check_for_new_riders(self, rider_list_csv, elevator_bank, floor_dict):
        for rider in rider_list_csv:
            if rider.when_to_add < (time() - elevator_bank.begin_time):
                rider.press_button(floor_dict)

    def log_movement(self, rider_names_to_add, rider_names_to_remove, log_dict):
        log_str = []
        rider_names_to_add.sort()
        rider_names_to_remove.sort()
        log_str.append(self.floor)
        log_str.append(self.direction)
        log_str.append(",".join(rider_names_to_add))
        log_str.append(",".join(rider_names_to_remove))
        log_dict[threading.current_thread().name].append(
            ";".join([str(log_element) for log_element in log_str])
        )
        return ";".join([str(log_element) for log_element in log_str])

    def let_riders_out(
        self,
        rider_list,
        start_stop_delays,
        start_step_delays,
    ):
        riders_to_remove = []
        rider_names_to_remove = []
        door_open = False
        if self.floor in self.internal_destinations:
            self.internal_destinations.remove(self.floor)  # ding, we stop
            for rider in self.riders:  # can we DRY?
                if rider.destination == self.floor:
                    riders_to_remove.append(rider)
                    rider_names_to_remove.append(str(rider))
                    # try:
                    rider_list.remove(rider)
                    # except ValueError:
                    #   pass
                    rider.step_out(start_stop_delays, start_step_delays)
                    door_open = True

        for rider in riders_to_remove:
            self.riders.remove(rider)

        # check if the rider who got off was the last one
        # if not rider_list:
        #     if not (self.direction == 0):
        #         self.direction = 0
        return door_open, rider_names_to_remove

    def update_direction(self, floor_dict):
        keep_going_down = False
        keep_going_up = False
        if self.internal_destinations:
            pass
        else:
            for floor in floor_dict.values():
                if isinstance(
                    floor, Floor
                ):  # there is a value in the dict that is not a Floor but rather a Boolean
                    if keep_going_down and keep_going_up:
                        break
                    if floor.number > self.floor and (
                        floor.up_request or floor.down_request
                    ):
                        keep_going_up = True
                    elif floor.number < self.floor and (
                        floor.up_request or floor.down_request
                    ):
                        keep_going_down = True
                    elif floor.number == self.floor and (
                        self.direction > -1 and floor.up_request
                    ):
                        keep_going_up = True
                    elif floor.number == self.floor and (
                        self.direction < 1 and floor.down_request
                    ):
                        keep_going_down = True
                    else:
                        continue

            if (keep_going_down and self.direction == -1) or (
                keep_going_up and self.direction == 1
            ):
                pass
            elif (keep_going_down and self.direction == 1) or (
                keep_going_up and self.direction == -1
            ):
                self.direction = self.direction * -1
            elif self.direction == 0 and keep_going_down:
                self.direction = -1
            elif (
                self.direction == 0 and keep_going_up
            ):  # would these two lines imply that keep_going_up has priority?
                self.direction = 1
            else:
                self.direction = 0

    def let_riders_in(self, floor_dict):
        clear_up_button = False
        clear_down_button = False
        door_open = False
        riders_to_step_in = []
        rider_names_to_add = []
        for rider in floor_dict[self.floor].riders:
            if self.direction == 1 and rider.destination > self.floor:  # going up
                if rider.step_in_no_capacity_check(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    clear_up_button = True
                door_open = True
            elif self.direction == -1 and rider.destination < self.floor:  # going down
                if rider.step_in_no_capacity_check(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    clear_down_button = True
                door_open = True
            else:
                pass
        # remove Rider from Floor if they are going in Elevator
        floor_dict[self.floor].riders = [
            e for e in floor_dict[self.floor].riders if e not in riders_to_step_in
        ]
        if clear_up_button:
            floor_dict[self.floor].up_request = False
        if clear_down_button:
            floor_dict[self.floor].down_request = False
        return door_open, rider_names_to_add


class NormalElevator(Elevator):
    def __init__(self, capacity: int, floor):
        self.floor = floor
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.internal_destinations = set(int)  # Set of ints
        self.door_delay = 1
        self.elevator_delay = 0.5
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did


class DestinationElevator(Elevator):
    def __init__(self, capacity: int, floor):
        self.floor = floor
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.destination = -1  # current dispatched destination
        self.door_delay = 1
        self.elevator_delay = 0.5
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did


class Rider:
    def __init__(self, name, destination, start_floor):
        self.name = name
        self.destination = destination
        self.start_floor = start_floor
        self.curr_floor = start_floor
        self.when_to_add = 0
        self.start_time = time()
        self.step_in_time = 0
        self.end_time = 0
        self.is_in_elevator = False
        self.button_pressed = False

    def __str__(self):
        return self.name  # for logging

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev):  # elevator should stop for a time even if full
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
            return False
        else:
            self.step_in_time = time()
            self.is_in_elevator = True
            elev.riders.append(self)
            return True

    def step_in_no_capacity_check(
        self, elev
    ):  # elevator should stop for a time even if full
        self.step_in_time = time()
        self.is_in_elevator = True
        elev.riders.append(self)
        return True

    def step_out(self, start_stop_delays, start_step_delays):
        self.end_time = time()
        start_stop_delays.append(self.end_time - self.start_time)
        start_step_delays.append(self.step_in_time - self.start_time)

    def press_button(self, floor_dict):
        self.button_pressed = True
        floor_dict[self.start_floor].riders.append(self)
        if self.start_floor < self.destination:
            floor_dict[self.start_floor].up_request = True
        else:
            floor_dict[self.start_floor].down_request = True

    def press_button_new(self, e_bank: ElevatorBank):
        nearest_elevator = self.find_nearest_available_elevator(e_bank)
        if nearest_elevator:
            nearest_elevator.external_destinations.append(self.start_floor)

    def find_nearest_available_elevator(self, elevator_bank: ElevatorBank) -> Elevator:
        """
        Returns the Elevator object that is the nearest (in terms of Floors)
        elevator that can pick up a rider. Elevator will probably be stationary,
        but can also return an Elevator that is on its way to the Rider's Floor,
        meaning has the proper direction and has a destination past the Rider's
        floor.

        If two elevators are equidistant then the higher elevator
        gets preference.

        Used for an elevator bank.
        """
        available_elevators = []
        for e in elevator_bank.elevators:
            if e.direction == 0:
                available_elevators.append(e)
            if (
                self.destination > self.start_floor
                and (e.direction == 1)  # elevator going up
                and (e.floor < self.start_floor)
            ):
                available_elevators.append(e)
            if (
                self.destination < self.start_floor
                and (e.direction == -1)  # elevator going down
                and (e.floor > self.start_floor)
            ):
                available_elevators.append(e)

        if not available_elevators:
            elevator_bank.queue.put(self.start_floor)
            return

        min_distance = abs(
            min(
                available_elevators, key=lambda x: abs(x.floor - self.start_floor)
            ).floor
            - self.start_floor
        )
        for e in available_elevators:  # higher elevators win tiebreaker
            if e.floor - self.start_floor == min_distance:
                return e
        for e in available_elevators:
            if self.start_floor - e.floor == min_distance:
                return e


class Floor:
    def __init__(self, number: int):
        self.number = number  # is this necessary if we have a dict of floors?
        self.riders = []
        self.has_elevator = False
        self.up_request = False
        self.down_request = False

    def __repr__(self):
        return f"Floor {self.number} has riders {[str(rider) for rider in self.riders]} and has {self.up_request} up request and {self.down_request} down request"
