from dataclasses import dataclass
from time import sleep, time
from sys import maxsize
import csv
from typing import Set
import tkinter as tk


# should I add a Building class which contains the Floor dict and
# a list of Elevators?


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

    def elevate(self, rider_list, floor_dict, start_stop_delays, start_step_delays):
        """
        Tells an elevator to pick up and drop off passengers
        given a rider list.

        Returns a string that represents the actions taken by
        the elevator.
        """
        root = tk.Tk()
        root.geometry("250x170")
        var = tk.StringVar()
        l = tk.Label(root, textvariable=var)
        l.pack()
        full_log = []
        while True:
            for rider in self.riders:
                rider.curr_floor = self.floor

            # to log what elevator does
            rider_names_to_remove = []
            rider_names_to_add = []

            # check if we are at an internal stop (someone inside wants to get off)
            door_open_out = self.let_riders_out(
                rider_names_to_add,
                rider_names_to_remove,
                rider_list,
                start_stop_delays,
                start_step_delays,
            )

            ## change direction if necessary
            # TODO: implement stopping logic
            self.update_direction(floor_dict)

            door_open_in = self.let_riders_in(floor_dict, rider_names_to_add)

            self.log = self.log_movement(
                rider_names_to_add,
                rider_names_to_remove,
            )
            self.floor += self.direction
            if door_open_in or door_open_out:
                sleep(self.door_delay)
            sleep(self.elevator_delay)
            # Tkinter stuff
            var.set(self.log)
            root.update_idletasks()
            print(self.log)
            full_log.append(self.log)

    def log_movement(
        self,
        rider_names_to_add,
        rider_names_to_remove,
    ):
        log = []
        rider_names_to_add.sort()
        rider_names_to_remove.sort()
        log.append(self.floor)
        log.append(self.direction)
        log.append(",".join(rider_names_to_add))
        log.append(",".join(rider_names_to_remove))
        return ";".join([str(log_element) for log_element in log])

    def let_riders_out(
        self,
        rider_names_to_add,
        rider_names_to_remove,
        rider_list,
        start_stop_delays,
        start_step_delays,
    ):
        riders_to_remove = []
        door_open = False
        if self.floor in self.internal_destinations:
            self.internal_destinations.remove(self.floor)  # ding, we stop
            for rider in self.riders:  # can we DRY?
                if rider.destination == self.floor:
                    riders_to_remove.append(rider)
                    rider_names_to_remove.append(str(rider))
                    rider_list.remove(rider)
                    rider.step_out(start_stop_delays, start_step_delays)
                    door_open = True

        for rider in riders_to_remove:
            self.riders.remove(rider)

        # check if the rider who got off was the last one
        if not rider_list:
            if not (self.direction == 0):
                self.log = self.log_movement(
                    rider_names_to_add,
                    rider_names_to_remove,
                )
                print(self.log)
                sleep(self.door_delay)
                self.direction = 0
        return door_open

    def update_direction(self, floor_dict):
        keep_going_down = False
        keep_going_up = False
        if self.internal_destinations:
            pass
        else:
            for floor in floor_dict.values():
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
            elif self.direction == 0 and keep_going_up:
                self.direction = 1
            else:
                self.direction = 0

    def let_riders_in(self, floor_dict, rider_names_to_add):
        clear_up_button = False
        clear_down_button = False
        door_open = False
        riders_to_step_in = []
        for rider in floor_dict[self.floor].riders:
            if self.direction == 1 and rider.destination > self.floor:  # going up
                rider.step_in(self)
                rider_names_to_add.append(str(rider))
                self.internal_destinations.add(rider.destination)
                riders_to_step_in.append(rider)
                clear_up_button = True
                door_open = True
            elif self.direction == -1 and rider.destination < self.floor:  # going down
                rider.step_in(self)
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
        return door_open


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
        self.start_time = time()
        self.step_in_time = 0
        self.end_time = 0
        self.is_in_elevator = False

    def __str__(self):
        return self.name  # for logging

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev):  # elevator should stop for a time even if full
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
        else:
            self.step_in_time = time()
            elev.riders.append(self)

    def step_out(self, start_stop_delays, start_step_delays):
        self.end_time = time()
        start_stop_delays.append(self.end_time - self.start_time)
        start_step_delays.append(self.step_in_time - self.start_time)

    def press_button(self, floor_dict):
        if self.start_floor < self.destination:
            floor_dict[self.start_floor].up_request = True
        else:
            floor_dict[self.start_floor].down_request = True


class Floor:
    def __init__(self, number: int):
        self.number = number  # is this necessary if we have a dict of floors?
        self.riders = []
        self.has_elevator = False
        self.up_request = False
        self.down_request = False

    def __repr__(self):
        return f"Floor {self.number} has riders {[str(rider) for rider in self.riders]} and has {self.up_request} up request and {self.down_request} down request"
