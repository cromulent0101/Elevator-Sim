# pylint: disable=import-error
from classes import Elevator, Rider
from time import sleep
from sys import maxsize
import random


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


print(find_next_floor(1, (1, 500, 3, 5, 4)))


def find_nearest_available_elevator(rider, elevator_bank) -> Elevator:
    """
    Returns an Elevator object that is the nearest (in terms of floors)
    elevator that can pick up a rider. Elevator will probably be stationary,
    but can also return an Elevator that is on its way to the Rider's floor,
    meaning has the proper direction and has a destination past the Rider's
    floor.
    """
    available_elevators = []
    for e in elevator_bank:
        if e.direction == 0:
            available_elevators.append(e)
        if any(rider.destination < dest for dest in e.destinations) and ( # elevator going up
            e.direction == 1) and (
            e.floor < rider.start_floor
        ):
            available_elevators.append(e)
        if any(rider.destination > dest for dest in e.destinations) and ( # elevator going down
            e.direction == -1)  and (
            e.floor > rider.start_floor
        ):
            available_elevators.append(e)
    min(available_elevators, key=lambda x:abs(x-rider.start_floor))

e1 = Elevator(3, 10)
e1.destinations = set(5)
e2 = Elevator(3, 20)
e2.destinations = set(15, 1)
e3 = Elevator(3, 13)
e3.destinations = set(13,30,40)


# prompt user to create a few riders, tracking highest and lowest floors of all types (dest and start)
rider_list = []
lowest_rider_floor = maxsize
highest_rider_floor = 0
while True:
    try:
        rider_name = input("Enter a rider name: ")
        rider_start_floor = int(input("Enter the rider's starting floor: "))
        rider_dest_floor = int(input("Enter the rider's destination: "))
        rider_list.append(Rider(rider_name, rider_dest_floor, rider_start_floor))
        if (
            rider_start_floor < lowest_rider_floor
            or rider_dest_floor < lowest_rider_floor
        ):
            lowest_rider_floor = min(rider_dest_floor, rider_start_floor)
        if (
            rider_start_floor > highest_rider_floor
            or rider_dest_floor > highest_rider_floor
        ):
            highest_rider_floor = max(rider_dest_floor, rider_start_floor)
    except ValueError as err:
        print("Terminating because", err)
        break
    except EOFError:
        print("EOF!")
        break

# create an elevator at some floor
e = Elevator(3, random.randint(lowest_rider_floor, highest_rider_floor))


for rider in rider_list:
    print(rider)

# to begin, all riders call an elevator to their start_floor at once
# this gotta change once I add more than one elevator
for rider in rider_list:
    e.destinations.add(rider.start_floor)

# arbitrarily choose elevator to go up first
e.direction = 1

## (single) elevator-centric algorithm - this should update every time elevator moves a floor
while True:
    # update elevator's riders' floors
    for rider in e.riders:
        rider.curr_floor = e.floor

    # I'm pretty sure I can combine the two following loops...
    # if the current floor is a destinaton, we MUST stop
    # riders with that destination get off
    riders_to_remove = []
    if e.floor in e.destinations:
        for rider in e.riders:
            if rider.destination == e.floor:
                riders_to_remove.append(rider)
                rider_list.remove(rider)
                print(
                    f"rider {rider.name} arrived at destination {rider.destination} and is at floor {e.floor}"
                )
                sleep(1)
        e.destinations.remove(e.floor)
    for rider in riders_to_remove:
        e.riders.remove(rider)

    if not rider_list:
        break

    # we don't know the direction of the  static elevator until the new rider's destination is added
    if not e.destinations:
        e.direction = 0

    # see if anyone needs to get on (in the elevator's direction), and add their destinations
    for rider in rider_list:
        if rider.start_floor == e.floor:
            if (rider.destination > e.floor and e.direction > -1) or (
                rider.destination < e.floor and e.direction < 1
            ):
                e.riders.append(rider)
                if rider.start_floor in e.destinations:
                    e.destinations.remove(rider.start_floor)
                e.destinations.add(rider.destination)
                print(
                    f"rider {rider.name} got on at floor {e.floor} going to {rider.destination}"
                )
                sleep(1)

    # update elevator's direction if there are no more destinations higher/lower than current floor
    if all(e.floor > dest for dest in e.destinations) and e.direction > -1:
        e.direction = -1
        print(
            f"elevator reached floor {e.floor}, turned around, and is now going {e.direction}"
        )
        sleep(1)
    elif all(e.floor < dest for dest in e.destinations) and e.direction < 1:
        e.direction = 1
        print(
            f"elevator reached floor {e.floor}, turned around, and is now going {e.direction}"
        )
        sleep(1)

    # at this point, doors close and we move again
    e.floor += e.direction
    print(f"elevator moved to floor {e.floor}")
    sleep(1)
