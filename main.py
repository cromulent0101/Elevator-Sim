# pylint: disable=import-error
from classes import Elevator,Rider
from time import sleep

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

# # create all floors in between min and max # of the floors - one per Floor
# print(f"creating floors {lowest_rider_floor} through {highest_rider_floor}")
# floor_list = []
# for floor in range(lowest_rider_floor,highest_rider_floor):
#     floor_list.append(Floor(floor))

# create an elevator at some floor
e = Elevator(3,1)


for rider in rider_list:
    print(rider)

# to begin, all riders call an elevator to their start_floor at once
# this gotta change once I add more than one elevator
for rider in rider_list:
    e.destinations.add(rider.start_floor)

# arbitrarily choose elevator to go up first
e.direction = 1

## elevator-centric algorithm - this should update every time elevator moves a floor
while True:
    # update elevator's riders' floors
    for rider in e.riders:
        rider.curr_floor = e.floor
    
    print(f"rider_list is {len(rider_list)}")



# I'm pretty sure I can combine the two following loops...
    # see if anyone should get off, remove the destination from elevator destinations, and kill rider
    # if the current floor is a destinaton, we MUST stop
    # riders with that destination get off
    riders_to_remove = []
    if e.floor in e.destinations:
        for rider in e.riders:
            if rider.destination == e.floor:
                riders_to_remove.append(rider)
                rider_list.remove(rider)
                print(f"rider {rider.name} arrived at destination {rider.destination} and is at floor {e.floor}")
                sleep(1)
        e.destinations.remove(e.floor) # we can't remove a destination twice if it's someone's final floor and someone's starting floor
    for rider in riders_to_remove:
        e.riders.remove(rider)
        
    if not rider_list: break
    if not e.destinations:
        e.direction = 0
    # update elevator's direction if there are no more destinations higher/lower than current floor
    # having this here solves case where elebator needs to turn around at the top,
    # but fails to get the top person when every passenger wants to go only one up

    # we don't know the direction of the elevator until the new rider's destination is added
    # imple solution: concept of a stationary elevator
    # see if anyone needs to get on (in the elevator's direction), and add their destinations
    for rider in rider_list:
        if rider.start_floor == e.floor:
            if (rider.destination > e.floor and e.direction > -1) or (rider.destination < e.floor and e.direction < 1): # this line is wrong
                e.riders.append(rider)
                if rider.start_floor in e.destinations:
                    e.destinations.remove(rider.start_floor) # how to handle when one person gets off and another gets in/
                e.destinations.add(rider.destination)
                print(f"rider {rider.name} got on at floor {e.floor} going to {rider.destination}")
                sleep(1)
    
    if (all(e.floor > dest for dest in e.destinations) and e.direction>-1):
        e.direction = -1
        print(f"elevator reached floor {e.floor}, turned around, and is now going {e.direction}")
        sleep(1)
    elif (all(e.floor < dest for dest in e.destinations) and e.direction<1):
        e.direction = 1
        print(f"elevator reached floor {e.floor}, turned around, and is now going {e.direction}")
        sleep(1)

    

    # at this point, doors close and we move again
    e.floor += e.direction
    print(f"elevator moved to floor {e.floor}")
    sleep(1)