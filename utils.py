# pylint: disable=import-error
from classes import Elevator, Rider, Floor, ElevatorBank
from typing import List, Dict
import csv
import logging

# import pandas as pd


def find_nearest_available_elevator(rider, elevator_bank: ElevatorBank) -> Elevator:
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
            rider.destination > rider.start_floor
            and (e.direction == 1)  # elevator going up
            and (e.floor < rider.start_floor)
        ):
            available_elevators.append(e)
        if (
            rider.destination < rider.start_floor
            and (e.direction == -1)  # elevator going down
            and (e.floor > rider.start_floor)
        ):
            available_elevators.append(e)

    if not available_elevators:
        elevator_bank.queue.put(rider.start_floor)
        return

    min_distance = abs(
        min(available_elevators, key=lambda x: abs(x.floor - rider.start_floor)).floor
        - rider.start_floor
    )
    for e in available_elevators:  # higher elevators win tiebreaker
        if e.floor - rider.start_floor == min_distance:
            return e
    for e in available_elevators:
        if rider.start_floor - e.floor == min_distance:
            return e


def get_riders_from_user() -> List[Rider]:
    """Returns a list of Riders on multiple floors from user input."""
    rider_list = []
    while True:
        try:
            rider_name = input("Enter a rider name: ")  # needs to be unique
            rider_start_floor = int(input("Enter the rider's starting floor: "))
            rider_dest_floor = int(input("Enter the rider's destination: "))
            rider_list.append(Rider(rider_name, rider_dest_floor, rider_start_floor))

        except ValueError as err:
            print("Terminating because", err)
            return
        except EOFError:
            print("EOF!")
            return rider_list


def update_riders_from_user(
    rider_list, floor_dict, elevator_bank
):  # TODO: revisit this with addition of destination control
    while True:
        try:
            rider_name = input("Enter a rider name: ")  # needs to be unique
            rider_start_floor = int(input("Enter the rider's starting floor: "))
            rider_dest_floor = int(input("Enter the rider's destination: "))
            new_rider = Rider(rider_name, rider_dest_floor, rider_start_floor)
            rider_list.append(new_rider)
            floor_dict[rider_start_floor].riders.append(new_rider)
            new_rider.press_button(floor_dict)
            nearest_elevator = find_nearest_available_elevator(new_rider, elevator_bank)
            nearest_elevator.external_destinations.add(rider_start_floor)
        except ValueError as err:
            print("Terminating because", err)
            return
        except EOFError:
            print("EOF!")
            return


def get_riders_from_csv(filename) -> List[Rider]:
    """
    Returns a list of Riders by parsing a CSV.
    """
    rider_list = []
    with open(filename, newline="") as csvfile:
        rider_reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in rider_reader:
            new_rider = Rider(
                row["name"], int(row["destination"]), int(row["start_floor"])
            )
            new_rider.when_to_add = int(row["when_to_add"])
            rider_list.append(new_rider)

    return rider_list


def get_riders_from_string(riders: str) -> List[Rider]:
    """
    Takes a newline-delimited list of riders, which are
    sub-delimited by semicolons, and returns a list of Riders.

    Each Rider is in the format:

    name;start_floor;destination;when_to_add
    """
    logging.debug(riders)
    rider_list = []
    for line in riders.split("\n"):
        rider_data = line.split(";")
        new_rider = Rider(rider_data[0], int(rider_data[1]), int(rider_data[2]))
        new_rider.when_to_add = int(rider_data[3])
        rider_list.append(new_rider)

    return rider_list


def create_floors(
    rider_list: List[Rider], elevator_bank: List[Elevator]
) -> Dict[int, Floor]:
    """
    Returns a dict of Floors initialized by a list of riders
    and presses buttons on those floors.
    """
    min_start_floor = min([rider.start_floor for rider in rider_list])
    min_destination = min([rider.destination for rider in rider_list])
    max_start_floor = max([rider.start_floor for rider in rider_list])
    max_destination = max([rider.destination for rider in rider_list])
    min_elevator = min([elevator.floor for elevator in elevator_bank])
    max_elevator = max([elevator.floor for elevator in elevator_bank])
    min_floor = min([min_start_floor, min_destination, min_elevator])
    max_floor = max([max_start_floor, max_destination, max_elevator])

    floor_dict = {}
    # populate dict of floors with each floor traversable and press up or down buttons on those floors
    for floor_num in range(min_floor - 1, max_floor + 2):
        floor_dict[floor_num] = Floor(floor_num)
    return floor_dict


# def test_helper(log_dict: dict) -> List[bool]:
#     for elev in log_dict.values():
#         split_elev = [row.split(";") for row in elev]
#         df = pd.DataFrame(
#             split_elev,
#             columns=["floor", "direction", "riders_in", "riders_out", "time"],
#         )
#         print(df)
