from dataclasses import dataclass
from time import sleep
from sys import maxsize
import csv


def find_next_floor(curr_floor, destinations):
    up_floor = maxsize
    down_floor = maxsize
    for floor in destinations:
        if floor > curr_floor:  # find closest floor above
            if abs(floor - curr_floor) < abs(up_floor - curr_floor):
                up_floor = floor
        if floor < curr_floor:  # find closest floor below
            if abs(floor - curr_floor) < abs(down_floor - curr_floor):
                down_floor = floor
    return down_floor, up_floor


# @dataclass
class InefficientElevator:
    def __init__(self, capacity: int, floor):
        self.floor = floor
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.destinations = set()  # Set of ints
        self.door_speed = 1
        self.elevator_speed = 10
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did

    def run(self, rider_list) -> str:
        """
        Tells and elevator to pick up and drop off passengers
        given a rider list.
        Returns a string that represents the actions taken by
        the elevator.
        """
        full_log = []
        while True:
            for rider in self.riders:
                rider.curr_floor = self.floor

            # to log what elevator does for testing
            starting_floor = self.floor
            starting_direction = self.direction
            rider_names_to_remove = []
            rider_names_to_add = []
            riders_to_remove = []
            ## decision: implement an up destinatoin list and a down one
            if self.floor in self.destinations:
                self.destinations.remove(self.floor)  # ding
                for rider in self.riders:
                    if rider.destination == self.floor:
                        riders_to_remove.append(rider)
                        rider_names_to_remove.append(str(rider))
                        rider_list.remove(rider)
                        # try:
                        #     self.destinations.remove(self.floor)
                        # except: pass
                for (
                    rider
                ) in rider_list:  # hacky way of re-adding floors we need to go back to
                    if rider.start_floor == self.floor and (
                        (rider.destination > self.floor and self.direction == -1)
                        or (rider.destination < self.floor and self.direction == 1)
                    ):
                        self.destinations.add(self.floor)
            for rider in riders_to_remove:
                self.riders.remove(rider)

            if not rider_list:
                rider_names_to_add.sort()
                rider_names_to_remove.sort()
                self.log = self.log_movement(
                    starting_floor,
                    starting_direction,
                    rider_names_to_add,
                    rider_names_to_remove,
                )
                full_log.append(self.log)
                return full_log

            # direction update if we're at top
            if (
                all(self.floor > dest for dest in self.destinations)
                and self.direction == 1
            ):  # maybe also check if car is empty and has reached a destination?
                self.direction = 0
            # if we're at bottom
            elif (
                all(self.floor < dest for dest in self.destinations)
                and self.direction == -1
            ):
                self.direction = 0

            # see if anyone needs to get on (in the elevator's direction), and add their destinations
            for rider in rider_list:
                if rider.start_floor == self.floor and (
                    (rider.destination > self.floor and self.direction == 1)
                    or (rider.destination < self.floor and self.direction == -1)
                    or (self.direction == 0)
                ):
                    self.riders.append(rider)
                    rider_names_to_add.append(str(rider))
                    self.destinations.add(rider.destination)
                # direction check if anyone got on -- priority to first person on
                if all(self.floor > dest for dest in self.destinations):
                    self.direction = -1

                elif all(self.floor < dest for dest in self.destinations):
                    self.direction = 1

            rider_names_to_add.sort()
            rider_names_to_remove.sort()
            self.log = self.log_movement(
                starting_floor,
                starting_direction,
                rider_names_to_add,
                rider_names_to_remove,
            )
            self.floor += self.direction
            full_log.append(self.log)

    def log_movement(
        self,
        starting_floor,
        starting_direction,
        rider_names_to_add,
        rider_names_to_remove,
    ):
        log = []
        log.append(starting_floor)
        log.append(starting_direction)
        log.append(",".join(rider_names_to_add))
        log.append(",".join(rider_names_to_remove))
        return ";".join([str(log_element) for log_element in log])


class Rider:
    def __init__(self, name, destination, start_floor):
        self.name = name
        self.destination = destination
        self.start_floor = start_floor
        self.curr_floor = start_floor
        self.is_in_elevator = False

    def __str__(self):
        return self.name  # for logging

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev):
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
        else:
            elev.riders.append(self)

    def press_button(self, destination):
        pass


# class Floor:
#     def __init__(self,number: int):
#         self.number = number
#         self.riders = []
#         self.has_elevator = False
#         self.up_request = False
#         self.down_request = False

#         def call_up(self,elev):
#             elev.destinations.add(self.number)

#         def call_down(self,elev):
#             elev.destinations.add(self.number)
