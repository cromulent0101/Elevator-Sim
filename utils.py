# pylint: disable=import-error
from classes import Elevator, Rider
from sys import maxsize


def find_nearest_available_elevator(rider, elevator_bank: list[Elevator]) -> Elevator:
    """
    Returns an Elevator object that is the nearest (in terms of floors)
    elevator that can pick up a rider. Elevator will probably be stationary,
    but can also return an Elevator that is on its way to the Rider's floor,
    meaning has the proper direction and has a destination past the Rider's
    floor.

    Used for an elevator bank.
    """
    available_elevators = []
    for e in elevator_bank:
        if e.direction == 0:
            available_elevators.append(e)
        if (
            any(rider.destination < dest for dest in e.destinations)
            and (e.direction == 1)  # elevator going up
            and (e.floor < rider.start_floor)
        ):
            available_elevators.append(e)
        if (
            any(rider.destination > dest for dest in e.destinations)
            and (e.direction == -1)  # elevator going down
            and (e.floor > rider.start_floor)
        ):
            available_elevators.append(e)
    return min(available_elevators, key=lambda x: abs(x - rider.start_floor))


def get_riders() -> list[Rider]:
    """Returns a list of Riders on multiple floors."""
    rider_list = []
    while True:
        try:
            rider_name = input("Enter a rider name: ")
            rider_start_floor = int(input("Enter the rider's starting floor: "))
            rider_dest_floor = int(input("Enter the rider's destination: "))
            rider_list.append(Rider(rider_name, rider_dest_floor, rider_start_floor))

        except ValueError as err:
            print("Terminating because", err)
            return
        except EOFError:
            print("EOF!")
            return rider_list


def get_min_max_floors(riders: list[Rider]) -> list:
    """
    Return the lowest and highest floors that a list
    of Riders could go to.
    """
    start_floors = [rider.start_floor for rider in riders]
    dest_floors = [rider.destination for rider in riders]
    highest_rider_floor = max(start_floors.extend(dest_floors))
    lowest_rider_floor = min(start_floors.extend(dest_floors))
    return [lowest_rider_floor, highest_rider_floor]
    # for rider in riders:
    #     if (
    #         rider_start_floor < lowest_rider_floor
    #         or rider_dest_floor < lowest_rider_floor
    #     ):
    #         lowest_rider_floor = min(rider_dest_floor, rider_start_floor)
    #     if (
    #         rider_start_floor > highest_rider_floor
    #         or rider_dest_floor > highest_rider_floor
    #     ):
    #         highest_rider_floor = max(rider_dest_floor, rider_start_floor)
