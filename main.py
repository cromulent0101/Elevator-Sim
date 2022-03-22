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

# create an elevator at bottom floor
e = Elevator(3,1)

# prompt user to create a few riders
rider_list = []
while True:
    try:
        rider_name = input("Enter a rider name: ")
        rider_start_floor = int(input("Enter the rider's starting floor: "))
        rider_dest_floor = int(input("Enter the rider's destination: "))
        rider_list.append(Rider(rider_name,rider_dest_floor,rider_start_floor))
    except ValueError as err:
        print('Terminating because', err)
        break
    except EOFError:
        print('EOF!')
        break

for rider in rider_list:
    print(rider)

# create all floors in between min and max # of the floors - one per Floor
floor_list = []
# have the riders call the elevator and try to get to their destination
while True:
    for rider in rider_list:
        if rider.destination != rider.curr_floor:
            break               # if one rider is not at his floor, do elevator things
        print("everyone is at their destination floor")
        break                   # break entire loop of elevator things once everyone is at their desired floor
    for rider in rider_list:
        if rider.curr_floor == rider.destination:
            continue
        # if rider.is_in_elevator


## elevator-centric algorithm - this should update every time elevator moves a floor

# we're at a new floor - remove current floor's requests
if e.direction == 1:
    e.floor.up_request = False
if e.direction == -1:
    e.floor.down_request = False


# see if any rider needs to get off
for rider in e.riders:
    if rider.destination == e.floor.number:
        e.riders.remove(rider)

# see if anyone needs to get on
for rider in rider_list:
    if rider.start_floor == e.floor.number:
        e.riders.add(rider)

# add new destinations for elevator
for floor in floor_list:
    if floor.up_request or floor.down_request:
        e.internal_destinations.add(floor.number)
for rider in e.riders:
    e.internal_destinations.add(rider.destination)

# find nearest destinations

down_dest,up_dest = find_next_floor(e.floor.number,e.destinations)

# close doors
# move elevator either up or down


