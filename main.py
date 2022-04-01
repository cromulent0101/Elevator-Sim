# pylint: disable=import-error
from classes import Elevator,Rider,Floor

no_floor = 123456789        # a very high number

def find_next_floor(curr_floor,destinations):
    up_floor = no_floor
    down_floor = no_floor
    for floor in destinations:
        if floor > curr_floor: # find closest floor above
            if abs(floor - curr_floor) < abs(up_floor - curr_floor):
                up_floor = floor
        if floor < curr_floor: # find closest floor below
            if abs(floor - curr_floor) < abs(down_floor - curr_floor):
                down_floor = floor
    return down_floor,up_floor
                            
print(find_next_floor(1,(1,500,3,5,4)))


# prompt user to create a few riders, tracking highest and lowest floors of all types (dest and start)
rider_list = []
lowest_rider_floor = no_floor
highest_rider_floor = 0
while True:
    try:
        rider_name = input("Enter a rider name: ")
        rider_start_floor = int(input("Enter the rider's starting floor: "))
        rider_dest_floor = int(input("Enter the rider's destination: "))
        rider_list.append(Rider(rider_name, rider_dest_floor, rider_start_floor))
        if rider_start_floor < lowest_rider_floor or rider_dest_floor < lowest_rider_floor:
            lowest_rider_floor = min(rider_dest_floor,rider_start_floor)
        if rider_start_floor > highest_rider_floor or rider_dest_floor > highest_rider_floor:
            highest_rider_floor = max(rider_dest_floor,rider_start_floor)
    except ValueError as err:
        print('Terminating because', err)
        break
    except EOFError:
        print('EOF!')
        break

# create all floors in between min and max # of the floors - one per Floor
print(f"creating floors {lowest_rider_floor} through {highest_rider_floor}")
floor_list = []
for floor in range(lowest_rider_floor,highest_rider_floor):
    floor_list.append(Floor(floor))

# create an elevator at bottom floor
e = Elevator(3,1)


for rider in rider_list:
    print(rider)


# have the riders call the elevator and try to get to their destination
while True:
    for rider in rider_list:
        if rider.destination != rider.curr_floor:
            break               # while one rider is not at his floor, do elevator things
        print("everyone is at their destination floor")
        break                   # break entire loop of elevator things once everyone is at their desired floor


## elevator-centric algorithm - this should update every time elevator moves a floor

# # we're at a new floor - remove current floor's requests
# if e.direction == 1 and all(e.floor > destfloor for destfloor in e.destinations):
#     e.floor.up_request = False
# if e.direction == -1:
#     e.floor.down_request = False

# we're at a new floor - remove old riders' destinations

# update riders' current floors

# check if we're stopping at this floor
if any(e.floor = dest for dest in e.destinations):
    

# see who should get off
for rider in e.riders:
    if rider.destination == e.floor:
        e.destinations.remove(rider.destination)            # destinations are floors
        e.riders.remove(rider)
        print(f"rider {rider.name} arrived at destination {rider.destination} and is at floor {e.floor.number}")

# see if anyone needs to get on
for rider in rider_list:
    if rider.start_floor == e.floor.number and rider.start_floor != rider.curr_floor:
        e.riders.add(rider)
        print(f"rider {rider.name} got on at floor {e.floor.number} going to {rider.destination}")

# add new destinations for elevator
# for floor in floor_list:
#     if floor.up_request or floor.down_request:
#         e.destinations.add(floor.number)
for rider in e.riders:
    e.destinations.add(rider.destination)       # rider destinations are only scalars?

# find nearest destinations

down_dest,up_dest = find_next_floor(e.floor.number,e.destinations)

# close doors

# move elevator either up or down

# update elevator's Floor


