class Elevator(self,capacity:int,floor:int): 
    self.direction = 'up'
    self.destination_queue = []
    self.door_speed = 1
    self.elevator_speed = 10
    self.is_moving = False
    self.riders = []

    def add_rider(Rider):
        self.riders.append(Rider)

    def remove_rider(Rider):
        self.riders.remove(Rider)

class Rider(self,name,destination:int):
    self.name = name 
    self.destination = destination
    self.curr_floor = 0

class Floor(self,number:int):
    self.number = number
    self.riders = []
    self.has_elevator = False
    self.up_request = False
    self.down_request = False


