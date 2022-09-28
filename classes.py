from dataclasses import dataclass
from time import sleep, time
from sys import maxsize
import csv


def find_next_floor(curr_floor, internal_destinations):
    up_floor = maxsize
    down_floor = maxsize
    for floor in internal_destinations:
        if floor > curr_floor:  # find closest floor above
            if abs(floor - curr_floor) < abs(up_floor - curr_floor):
                up_floor = floor
        if floor < curr_floor:  # find closest floor below
            if abs(floor - curr_floor) < abs(down_floor - curr_floor):
                down_floor = floor
    return down_floor, up_floor


# should I add a Building class which contains the Floor dict and
# a list of Elevators?

# @dataclass
class Elevator:
    def __init__(self, capacity: int, floor):
        self.floor = floor
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.internal_destinations = set()  # Set of ints
        self.door_delay = 1
        self.elevator_delay = 0.5
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did

    def elevate(
        self, rider_list, floor_dict, start_stop_delays, start_step_delays
    ) -> str:
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

            door_open = False  # if True, sleep(door_delay) once

            # check if we are at an internal stop (someone inside wants to get off)
            if self.floor in self.internal_destinations:
                self.internal_destinations.remove(self.floor)  # ding, we stop
                for rider in self.riders:  # can we DRY?
                    if rider.destination == self.floor:
                        riders_to_remove.append(rider)
                        rider_names_to_remove.append(str(rider))
                        rider_list.remove(rider)
                        rider.end_time = time()
                        start_stop_delays.append(rider.end_time - rider.start_time)
                        start_step_delays.append(rider.step_in_time - rider.start_time)
                        door_open = True

            for rider in riders_to_remove:
                self.riders.remove(rider)

            # check if the rider who got off was the last one
            if not rider_list:
                rider_names_to_add.sort()  # sort to ensure order is consistent
                rider_names_to_remove.sort()
                self.log = self.log_movement(
                    starting_floor,
                    starting_direction,
                    rider_names_to_add,
                    rider_names_to_remove,
                )
                full_log.append(self.log)
                print(self.log)
                sleep(self.door_delay)  # open door one last time
                return full_log

            ## change direction if necessary
            # TODO: implement stopping logic
            if self.internal_destinations:
                pass
            else:
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

                if (keep_going_down and self.direction == -1) or (
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
                    print(self.log)
                    return full_log

            # see if anyone needs to get on (in the elevator's direction), and add their internal_destinations
            clear_up_button = False
            clear_down_button = False
            riders_to_step_in = []
            for rider in floor_dict[self.floor].riders:
                if (
                    floor_dict[self.floor].up_request
                    and self.direction == 1
                    and rider.destination > self.floor
                ):  # going up, rider goes from floor into elevator and adds destination
                    rider.step_in(self)
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(
                        rider.destination
                    )  # should be greater than self.floor
                    riders_to_step_in.append(rider)
                    clear_up_button = True
                    door_open = True

                elif (
                    floor_dict[self.floor].down_request
                    and self.direction == -1
                    and rider.destination < self.floor
                ):  # going down
                    rider.step_in(self)
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(
                        rider.destination
                    )  # should be less than self.floor
                    riders_to_step_in.append(rider)
                    clear_down_button = True
                    door_open = True

                else:
                    pass

            floor_dict[self.floor].riders = [
                e for e in floor_dict[self.floor].riders if e not in riders_to_step_in
            ]

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
            if door_open:
                sleep(self.door_delay)
            sleep(self.elevator_delay)
            print(self.log)
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


class DestinationElevator:
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
