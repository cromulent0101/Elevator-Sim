class Elevator(self,capacity,floor): 
    self.direction = 0     # 0 for stationary, 1 for up, -1 for down
    self.destinations = ()
    self.door_speed = 1
    self.elevator_speed = 10
    self.riders = []

    def add_rider(Rider):
        self.riders.append(Rider)

    def remove_rider(Rider):
        self.riders.remove(Rider)

    def press_button(destination):
        pass

class Rider(self,name,destination):
    self.name = name 
    self.destination = destination
    self.curr_floor = 0

class Floor(self,number):
    self.number = number
    self.riders = []
    self.has_elevator = False
    self.up_request = False
    self.down_request = False

    def call_up(Elevator):
        Elevator.destinations.add(self.number)



