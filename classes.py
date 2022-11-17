from dataclasses import dataclass
from time import sleep, time
from sys import maxsize
from queue import Queue, Empty
import csv
from typing import Set
import tkinter as tk
import threading


class ElevatorBank:
    def __init__(self, elevator_list):
        self.elevators = elevator_list
        self.queue = Queue()  # floors that don't have an elevator going to them yet
        self.begin_time = time()

    def simulate(self, rider_list_csv, floor_dict):
        threads = []
        start_stop_delays = []
        start_step_delays = []
        log_dict = {}

        for e in self.elevators:
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
            )
            log_dict[t1.name] = []
            t1.start()
            threads.append(t1)
        for t in threads:  # TODO: investigate asyncio.gather()
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
        while True:
            # checking for new riders can be refactored out of Elevator
            self.check_for_new_riders(rider_list, e_bank, floor_dict)
            for rider in self.riders:
                rider.curr_floor = self.floor

            door_open_out, rider_names_to_remove = self.let_riders_out_new(
                rider_list, start_stop_delays, start_step_delays, log_dict
            )
            self.update_direction_new(e_bank)
            door_open_in, rider_names_to_add = self.let_riders_in_new(floor_dict)
            self.log = self.log_movement(
                rider_names_to_add, rider_names_to_remove, log_dict
            )
            self.floor += self.direction
            self.simulate_delays(door_open_in, door_open_out)
            print(self.log)

    def let_riders_out_new(
        self, rider_list, start_stop_delays, start_step_delays, log_dict
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
                    rider_list.remove(rider)
                    rider.step_out(start_stop_delays, start_step_delays)
                    door_open = True

        for rider in riders_to_remove:
            self.riders.remove(rider)

        # check if the rider who got off was the last one
        if not rider_list:
            if not (self.direction == 0):
                self.log = self.log_movement([], rider_names_to_remove, log_dict)
                print(self.log)
                sleep(self.door_delay)
                # self.direction = 0
        return door_open, rider_names_to_remove

    def update_direction_new(self, e_bank: ElevatorBank):
        if (
            (self.internal_destinations or self.external_destinations)
            and self.direction != 0
            and not self.floor in self.external_destinations
        ):
            # #print(
            #     f"internal dest {self.internal_destinations} or external dest {self.external_destinations} w dir"
            # )
            pass
        elif self.external_destinations and self.direction == 0:
            # print(f"ext dest {self.external_destinations} but stationary")
            if (
                list(self.external_destinations)[0] > self.floor
            ):  # assuming only one external dest would be added at once
                self.direction = 1
            elif list(self.external_destinations)[0] < self.floor:
                self.direction = -1
        elif self.internal_destinations and self.direction == 0:
            # print(f"internal dest {self.internal_destinations} but stationary")
            if (
                list(self.internal_destinations)[0] > self.floor
            ):  # assuming only one external dest would be added at once
                self.direction = 1
            elif list(self.internal_destinations)[0] < self.floor:
                self.direction = -1
        elif self.floor in self.external_destinations:
            self.direction = 0
        elif not e_bank.queue.empty():
            # print("went to elev queue")
            try:
                next_floor = e_bank.queue.get()
                if next_floor > self.floor:
                    self.direction = 1
                    self.external_destinations.add(next_floor)
                elif next_floor < self.floor:
                    self.direction = -1
                    self.external_destinations.add(next_floor)
            except Empty:
                pass
        else:
            self.direction = 0

    def let_riders_in_new(self, floor_dict):
        clear_up_button = False
        clear_down_button = False
        door_open = False
        riders_to_step_in = []
        rider_names_to_add = []
        for rider in floor_dict[self.floor].riders:
            if self.direction > -1 and rider.destination > self.floor:  # going up
                rider.step_in(self)
                rider_names_to_add.append(str(rider))
                self.internal_destinations.add(rider.destination)
                riders_to_step_in.append(rider)
                clear_up_button = True
                door_open = True
            elif self.direction < 1 and rider.destination < self.floor:  # going down
                rider.step_in(self)
                rider_names_to_add.append(str(rider))
                self.internal_destinations.add(rider.destination)
                riders_to_step_in.append(rider)
                clear_down_button = True
                door_open = True
            else:
                pass
        try:
            self.external_destinations.remove(self.floor)
        except KeyError:
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

    def simulate_delays(self, door_open_in, door_open_out):
        if door_open_in or door_open_out:
            sleep(self.door_delay)
        sleep(self.elevator_delay)

    def check_for_new_riders(self, rider_list_csv, elevator_bank, floor_dict):
        for rider in rider_list_csv:
            delta_time = time() - elevator_bank.begin_time
            if rider.when_to_add < (delta_time) and not (rider.button_pressed):
                floor_dict[rider.start_floor].riders.append(rider)
                rider.press_button_new(elevator_bank)

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
        self.button_pressed = False
        self.button_pressed_up = False
        self.button_pressed_down = False

    def __str__(self):
        return self.name  # for logging

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev):  # elevator should stop for a time even if full
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
        else:
            self.step_in_time = time()
            self.is_in_elevator = True
            elev.riders.append(self)

    def step_out(self, start_stop_delays, start_step_delays):
        self.end_time = time()
        start_stop_delays.append(self.end_time - self.start_time)
        start_step_delays.append(self.step_in_time - self.start_time)

    def press_button_new(self, e_bank: ElevatorBank):
        self.button_pressed = True
        nearest_elevator = self.find_nearest_available_elevator(e_bank)
        if nearest_elevator:
            nearest_elevator.external_destinations.add(self.start_floor)

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
