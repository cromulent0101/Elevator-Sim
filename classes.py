# pylint: disable=import-error
from dataclasses import dataclass
from time import sleep, time
from sys import maxsize
from random import randint
import csv
from typing import Set
import tkinter as tk
import threading


class ElevatorBank:
    def __init__(self, elevator_list):
        self.elevators = elevator_list
        self.queue = set()  # floors that don't have an elevator going to them yet
        self.begin_time = time()

    def simulate(self, rider_list_csv, floor_dict):
        threads = []
        rider_list = []
        start_stop_delays = []
        start_step_delays = []
        log_dict = {}
        rider_updater = threading.Thread(
            target=self.rider_update,
            args=[rider_list, rider_list_csv, floor_dict, self],
            name="Rider Updater",
        )
        rider_updater.start()
        threads.append(rider_updater)
        for idx, e in enumerate(self.elevators, start=1):
            log_dict[f"\x1b[1;3{idx};40m" + f"Elevator {idx}" + "\x1b[0m"] = []
            t1 = threading.Thread(
                target=e.elevate,
                args=[
                    rider_list,
                    floor_dict,
                    start_stop_delays,
                    start_step_delays,
                    self,
                    log_dict,
                ],
                name=f"\x1b[1;3{idx};40m" + f"Elevator {idx}" + "\x1b[0m",
            )
            sleep(0.001)
            t1.start()
            threads.append(t1)
        for t in threads:  # TODO: investigate asyncio.gather()
            t.join()

        return start_step_delays, start_stop_delays, log_dict

    def rider_update(self, rider_list, rider_list_csv, floor_dict, e_bank):
        floor_dict["done"] = False
        while rider_list_csv:
            for rider in rider_list_csv:
                if rider.when_to_add < (time() - e_bank.begin_time):
                    rider.press_button_new(self)
                    floor_dict[rider.start_floor].riders.append(rider)
                    rider_list.append(rider)
                    rider_list_csv.remove(rider)
        while rider_list:
            sleep(1)
        floor_dict["done"] = True


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

            self.destination_check(floor_dict)
            door_open_out, rider_names_to_remove = self.let_riders_out_new(
                rider_list, start_stop_delays, start_step_delays, log_dict
            )
            self.update_direction_new(e_bank)
            door_open_in, rider_names_to_add = self.let_riders_in_new(
                floor_dict, e_bank
            )
            self.log = self.log_movement(
                rider_names_to_add, rider_names_to_remove, log_dict
            )
            self.floor += self.direction
            self.simulate_delays(door_open_in, door_open_out)
            print(self.log)
            print(threading.current_thread().name)

    def destination_check(self, floor_dict):
        """
        Performs a sanity check on external destinations. If there is no rider at a Floor that is an external destination,
        remove it from the list of external destinations.
        """
        ext_dests_copy = self.external_destinations.copy()
        for floor in ext_dests_copy:
            if not floor_dict[floor].riders:
                self.external_destinations.remove(floor)

    def let_riders_out_new(
        self, rider_list, start_stop_delays, start_step_delays, log_dict
    ):
        """
        Lets riders out of the elevator, and adds a delay if anyone does.

        Also removes the current floor from both external and
        internal destinations.
        """
        riders_to_remove = []
        rider_names_to_remove = []
        door_open = False
        if self.floor in self.external_destinations:
            self.external_destinations.remove(self.floor)
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

        return door_open, rider_names_to_remove

    def update_direction_new(self, e_bank: ElevatorBank):
        if self.direction == 0:
            if e_bank.queue:
                print("went to elev queue")
                next_floor = self.find_nearest_floor(list(e_bank.queue))
                if next_floor > self.floor:
                    self.direction = 1
                    self.external_destinations.add(next_floor)
                elif next_floor < self.floor:
                    self.direction = -1
                    self.external_destinations.add(next_floor)
                try:
                    e_bank.queue.remove(next_floor)
                except KeyError:
                    pass
        elif self.internal_destinations or self.external_destinations:
            pass
        else:
            self.direction = 0

    def let_riders_in_new(self, floor_dict, e_bank):
        door_open = False
        riders_to_step_in = []
        rider_names_to_add = []

        for rider in floor_dict[self.floor].riders:
            if self.direction > -1 and rider.destination > self.floor:  # going up
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    door_open = True
                    try:
                        e_bank.queue.remove(self.floor)
                    except KeyError:
                        pass
                    self.direction = 1
                else:
                    rider.press_button_new(e_bank)
                    print("lool")
            elif self.direction < 1 and rider.destination < self.floor:  # going down
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    door_open = True
                    try:
                        e_bank.queue.remove(self.floor)
                    except KeyError:
                        pass
                    self.direction = -1
                else:
                    rider.press_button_new(e_bank)
                    print("lool")
            else:  # if there's an elevator at our floor but not in right direction
                rider.press_button_new(e_bank)

        # remove Rider from Floor if they are going in Elevator
        floor_dict[self.floor].riders = [
            e for e in floor_dict[self.floor].riders if e not in riders_to_step_in
        ]
        return door_open, rider_names_to_add

    def simulate_delays(self, door_open_in, door_open_out):
        if door_open_in or door_open_out:
            sleep(self.door_delay)
        sleep(self.elevator_delay)

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

    def find_nearest_floor(self, floor_queue):
        if floor_queue == None:
            return self.floor
        nearest_floor = maxsize
        for floor in floor_queue:
            if abs(floor - self.floor) < abs(nearest_floor - self.floor):
                nearest_floor = floor
        return nearest_floor


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


# see http://www.facilitiesnet.com/elevators/article/Destination-Dispatch-Machineroomless-Systems-Are-Current-Wave-of-Elevator-Technology--13595?source=previous
# and https://www.thyssenkruppelevator.com/elevator-products/elevator-destination-dispatch
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
        self.dispatched_elevator = False
        self.button_pressed_up = False
        self.button_pressed_down = False

    def __str__(self):
        return self.name  # for logging

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev):  # elevator should stop for a time even if full
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name: >20} can't enter elevator since it is full")
            return False
        else:
            self.step_in_time = time()
            self.is_in_elevator = True
            elev.riders.append(self)
            return True

    def step_out(self, start_stop_delays, start_step_delays):
        self.end_time = time()
        start_stop_delays.append(self.end_time - self.start_time)
        start_step_delays.append(self.step_in_time - self.start_time)

    def press_button_new(self, e_bank: ElevatorBank):
        nearest_elevator = self.find_nearest_available_elevator(e_bank)
        if nearest_elevator:
            nearest_elevator.external_destinations.add(self.start_floor)
            self.dispatched_elevator = nearest_elevator

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
            # if e.direction == 0:
            #     available_elevators.append(e)
            if (
                self.destination > self.start_floor
                and (e.direction == 1)  # elevator going up
                and (e.floor < self.start_floor)
            ):
                available_elevators.append(e)
            elif (
                self.destination < self.start_floor
                and (e.direction == -1)  # elevator going down
                and (e.floor > self.start_floor)
            ):
                available_elevators.append(e)

        if not available_elevators:
            elevator_bank.queue.add(self.start_floor)
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
