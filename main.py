from classes import Elevator

def find_next_floor(curr_floor,destinations):
    up_floor = 10000000
    down_floor = 10000000
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

# create all floors in between min and max # of the floors

# have the riders call the elevator and try to get to their destination
