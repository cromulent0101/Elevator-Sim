def find_next_floor(curr_floor,destinations):
    up_floor = 1
    down_floor = 1
    for floor in destinations:
        if floor > curr_floor: # find closest floor above
            if abs(floor - curr_floor) < abs(up_floor - curr_floor):
                up_floor = floor
        if floor < curr_floor: # find closest floor below
            if abs(floor - curr_floor) < abs(down_floor - curr_floor):
                down_floor = floor
    return down_floor,up_floor
                            
                            


class Elevator: 
    def __init__(self,capacity,floor):
        self.floor = floor
        self.capacity = capacity   
        self.direction = 0          # 0 for stationary, 1 for up, -1 for down
        self.internal_destinations = ()      # set of Floors
        self.door_speed = 1
        self.elevator_speed = 10
        self.riders = ()                    # set of Riders

    def find_next_floor(self,destinations):
        up_floor = 10000000
        down_floor = 10000000
        for floor in destinations:
            if floor > self.floor: # find closest floor above
                if abs(floor - self.floor) < abs(up_floor - self.floor):
                    up_floor = floor
            if floor < self.floor: # find closest floor below
                if abs(floor - self.floor) < abs(down_floor - self.floor):
                    down_floor = floor
        return down_floor,up_floor

    def stop_at_floor(self):
        for floor in self.destinations:
            if (self.floor > floor) and (self.direction < 1):  # going down
                pass

class Rider:
    def __init__(self,name,destination,start_floor):
        self.name = name 
        self.destination = destination
        self.start_floor = start_floor
        self.curr_floor = start_floor
        self.is_in_elevator = False

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self,elev):
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
        else:
            elev.riders.append(self)

    def press_button(self,destination):
        pass

class Floor:
    def __init__(self,number):
        self.number = number
        self.riders = []
        self.has_elevator = False
        self.up_request = False
        self.down_request = False

        def call_up(self,elev):
            elev.destinations.add(self.number)

        def call_down(self,elev):
            elev.destinations.add(self.number)


