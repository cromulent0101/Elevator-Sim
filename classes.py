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

    def run(self, rider_list, floor_dict) -> str:
        """
        Tells an elevator to pick up and drop off passengers
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
            ## decision: implement floors again
            # if we are at an internal stop (someone inside wants to get off)
            if self.floor in self.destinations:
                self.destinations.remove(self.floor)  # ding, we stop
                for rider in self.riders:  # can we DRY?
                    if rider.destination == self.floor:
                        riders_to_remove.append(rider)
                        rider_names_to_remove.append(str(rider))
                        rider_list.remove(rider)

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

            ## change direction if necessary
            # if there is an internal dest on the way, continue in that dir
            # if there not an internal dest on the way, turn around or stop
            # keep_going_up = any([floor.up_request for floor in list(floor_dict.values())])
            # keep_going_down = any([floor.down_request for floor in list(floor_dict.values())])
            keep_going_down = False
            keep_going_up = False
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
                    self.direction == 1 and floor.up_request
                ):
                    keep_going_up = True
                elif floor.number == self.floor and (
                    self.direction == -1 and floor.down_request
                ):
                    keep_going_down = True
                else:
                    continue

            if self.destinations:
                pass
            elif (keep_going_down and self.direction == -1) or (
                keep_going_up and self.direction == 1
            ):
                pass
            elif (keep_going_down and self.direction == 1) or (
                keep_going_up and self.direction == -1
            ):
                self.direction = self.direction * -1
            else:
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

            # see if anyone needs to get on (in the elevator's direction), and add their destinations
            clear_up_button = False
            clear_down_button = False
            for rider in floor_dict[self.floor].riders:
                if (
                    floor_dict[self.floor].up_request
                    and self.direction == 1
                    and rider.destination > self.floor
                ):  # going up, rider goes from floor into elevator and adds destination
                    rider.step_in(self)
                    rider_names_to_add.append(str(rider))
                    self.destinations.add(
                        rider.destination
                    )  # should be greater than self.floor
                    floor_dict[self.floor].riders.remove(rider)
                    clear_up_button = True
                elif (
                    floor_dict[self.floor].down_request
                    and self.direction == -1
                    and rider.destination < self.floor
                ):  # going down
                    rider.step_in(self)
                    rider_names_to_add.append(str(rider))
                    self.destinations.add(
                        rider.destination
                    )  # should be less than self.floor
                    floor_dict[self.floor].riders.remove(rider)
                    clear_down_button = True
                else:
                    pass
            floor_dict[self.floor].up_request = not clear_up_button
            floor_dict[self.floor].down_request = not clear_down_button

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


class Floor:
    def __init__(self, number: int):
        self.number = number  # is this necessary if we have a dict of floors?
        self.riders = []
        self.has_elevator = False
        self.up_request = False
        self.down_request = False

    def __repr__(self):
        return f"Floor {self.number} has riders {[str(rider) for rider in self.riders]} and has {self.up_request} up request and {self.down_request} down request"
