# pylint: disable=import-error
from classes import InefficientElevator, Rider, Floor
from sys import maxsize


def find_nearest_available_elevator(
    rider, elevator_bank: list[InefficientElevator]
) -> InefficientElevator:
    """
    Returns an Elevator object that is the nearest (in terms of Floors)
    elevator that can pick up a rider. Elevator will probably be stationary,
    but can also return an Elevator that is on its way to the Rider's Floor,
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
    """Returns a list of Riders on multiple floors from user input."""
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


def create_floors(rider_list: list[Rider]) -> dict[Floor]:
    """
    Returns a dict of Floors initialized by a list of riders
    and presses buttons on those floors.
    """
    min_start_floor = min([rider.start_floor for rider in rider_list])
    min_destination = min([rider.destination for rider in rider_list])
    max_start_floor = max([rider.start_floor for rider in rider_list])
    max_destination = max([rider.destination for rider in rider_list])
    min_floor = min([min_start_floor, min_destination])
    max_floor = max([max_start_floor, max_destination])

    floor_dict = {}
    # populate dict of floors with each floor traversable and press up or down buttons on those floors
    for floor_num in range(min_floor - 1, max_floor + 2):
        floor_dict[floor_num] = Floor(floor_num)
        for rider in rider_list:
            if rider.start_floor == floor_num:
                floor_dict[floor_num].riders.append(rider)
                if rider.start_floor > rider.destination:
                    floor_dict[floor_num].down_request = True
                else:
                    floor_dict[floor_num].up_request = True
    return floor_dict
