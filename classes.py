from time import sleep
from sys import maxsize
from typing import Tuple, List


class ElevatorBank:
    def __init__(self, elevator_list):
        self.elevators = elevator_list
        self.queue = (
            set()
        )  # set of floors that don't have an elevator going to them yet

    def simulate(self, rider_list_csv, floor_dict, time_step, max_time, elevate_type):
        sim_time = 0
        rider_list = []
        start_stop_delays = []
        start_step_delays = []
        floors_traversed = [0]
        log_dict = {}
        for elevator in self.elevators:
            log_dict[f"Elevator {elevator.name}"] = []
        floor_dict["done"] = False
        while not floor_dict["done"] and sim_time < max_time:
            for elevator in self.elevators:
                if (
                    elevator.simulated_time >= sim_time
                    and elevator.simulated_time < sim_time + time_step
                ):
                    getattr(
                        elevator, elevate_type
                    )(  # call different methods based on parameter. Should probably use OOP here
                        rider_list,
                        floor_dict,
                        start_stop_delays,
                        start_step_delays,
                        floors_traversed,
                        self,
                        log_dict,
                        rider_list_csv,
                    )
            sim_time = sim_time + time_step
        if sim_time > max_time:
            print(f"Simulation took more time than {max_time} ticks")
            raise Exception
        return start_step_delays, start_stop_delays, floors_traversed[-1], log_dict


class Elevator:
    def __init__(self, capacity: int, floor: int, name: str):
        self.floor = floor
        self.name = name
        self.capacity = capacity
        self.direction = 0  # 0 for stationary, 1 for up, -1 for down
        self.internal_destinations = set()
        self.external_destinations = set()
        self.door_delay = 1
        self.elevator_delay = 0.5
        self.simulated_time = 0
        self.riders = []  # list of Riders
        self.log = []  # list of strs to log what elevator did

    def __eq__(
        self, other
    ):  # FYI implementing this makes Elevators not be able to be in sets/dicts
        if not isinstance(other, Elevator):
            return NotImplemented

        return self.floor == other.floor and self.direction == other.direction

    def __str__(self):
        return f"{self.floor}  {self.direction}"

    def __repr__(self):
        return f"Elevator is on {self.floor} and direction {self.direction}"

    def elevate(
        self,
        rider_list,
        floor_dict,
        start_stop_delays,
        start_step_delays,
        floors_traversed,
        e_bank,
        log_dict,
        rider_list_csv,
    ) -> None:
        """
        Tells an elevator to pick up and drop off passengers
        given a rider list.

        Prints a string that represents the actions taken by
        the elevator.
        """
        self.check_for_new_riders(rider_list_csv, e_bank, floor_dict, rider_list)
        for rider in self.riders:
            rider.curr_floor = self.floor

        should_door_open_out, rider_names_to_remove = self.let_riders_out_new(
            rider_list, start_stop_delays, start_step_delays
        )
        self.update_direction_new(floor_dict)
        should_door_open_in, rider_names_to_add = self.let_riders_in_new(
            floor_dict, e_bank
        )
        self.log = self.log_movement(
            rider_names_to_add, rider_names_to_remove, log_dict
        )
        self.floor += self.direction
        floors_traversed.append(
            floors_traversed[-1] + abs(self.direction)
        )  # wish there was a better way to do this. can mutate?
        self.simulate_delays(should_door_open_in, should_door_open_out)
        # print(self.log)

    def elevate_floor(
        self,
        rider_list,
        floor_dict,
        start_stop_delays,
        start_step_delays,
        floors_traversed,
        e_bank,
        log_dict,
        rider_list_csv,
    ) -> None:
        """
        Tells an elevator to pick up and drop off passengers
        given a rider list.

        Prints a string that represents the actions taken by
        the elevator.
        """
        self.check_for_new_riders_floor(rider_list_csv, e_bank, floor_dict, rider_list)
        for rider in self.riders:
            rider.curr_floor = self.floor

        # self.destination_check(floor_dict)  # this sometimes has a very slight impact on output when not all Riders are added at once. TODO: explain it
        should_door_open_out, rider_names_to_remove = self.let_riders_out_new_floor(
            rider_list, start_stop_delays, start_step_delays
        )
        self.update_direction_new_floor(e_bank)
        should_door_open_in, rider_names_to_add = self.let_riders_in_new_floor(
            floor_dict, e_bank
        )
        self.log = self.log_movement(
            rider_names_to_add, rider_names_to_remove, log_dict
        )
        self.floor += self.direction
        floors_traversed.append(
            floors_traversed[-1] + abs(self.direction)
        )  # wish there was a better way to do this. can mutate?
        self.simulate_delays(should_door_open_in, should_door_open_out)
        # print(self.log)

    def check_for_new_riders(  # should be refactored out of Elevator and into ElevatorBank
        self, rider_list_csv, elevator_bank, floor_dict, rider_list
    ) -> None:
        rider_list_csv_copy = [] + rider_list_csv
        if not rider_list_csv and not rider_list:
            floor_dict["done"] = True
        else:
            for rider in rider_list_csv_copy:
                if rider.when_to_add <= self.simulated_time:
                    rider_list.append(rider)
                    floor_dict[rider.start_floor].riders.append(rider)
                    rider.press_button_new(floor_dict)
                    rider_list_csv.remove(rider)

    def check_for_new_riders_floor(  # should be refactored out of Elevator and into ElevatorBank
        self, rider_list_csv, elevator_bank, floor_dict, rider_list
    ) -> None:
        rider_list_csv_copy = [] + rider_list_csv
        if not rider_list_csv and not rider_list:
            floor_dict["done"] = True
        else:
            for rider in rider_list_csv_copy:
                if rider.when_to_add <= self.simulated_time:
                    rider_list.append(rider)
                    floor_dict[rider.start_floor].riders.append(rider)
                    rider.press_button_new_floor(elevator_bank)
                    rider_list_csv.remove(rider)

    def simulate_delays(self, should_door_open_in, should_door_open_out) -> None:
        """
        Increments the simulation timer based on the simulation time step
        and any delays introduced by opening the elevator door.

        Each time the elevator moves a floor or opens the door,
        the simulation timer should increment by some amount.
        """
        if should_door_open_in or should_door_open_out:
            self.simulated_time = self.simulated_time + self.door_delay
        self.simulated_time = self.simulated_time + self.elevator_delay

    def log_movement(self, rider_names_to_add, rider_names_to_remove, log_dict) -> str:
        log_str = []
        rider_names_to_add.sort()
        rider_names_to_remove.sort()
        log_str.append(self.floor)
        log_str.append(self.direction)
        log_str.append(",".join(rider_names_to_add))
        log_str.append(",".join(rider_names_to_remove))
        log_str.append(self.simulated_time)
        log_dict[f"Elevator {self.name}"].append(
            ";".join([str(log_element) for log_element in log_str])
        )
        return ";".join([str(log_element) for log_element in log_str])

    def let_riders_out_new(
        self, rider_list, start_stop_delays, start_step_delays
    ) -> Tuple[bool, List]:
        """
        Lets riders out of the elevator, and adds a delay if anyone does.

        Also removes the current floor from internal destinations.
        """
        riders_to_remove = []
        rider_names_to_remove = []
        should_door_open = False
        if self.floor in self.internal_destinations:
            self.internal_destinations.remove(self.floor)  # ding, we stop
            for rider in self.riders:  # can we DRY?
                if rider.destination == self.floor:
                    riders_to_remove.append(rider)
                    rider_names_to_remove.append(str(rider))
                    rider_list.remove(rider)
                    rider.step_out(self, start_stop_delays, start_step_delays)
                    should_door_open = True
        for rider in riders_to_remove:
            self.riders.remove(rider)
        return should_door_open, rider_names_to_remove

    def let_riders_out_new_floor(
        self, rider_list, start_stop_delays, start_step_delays
    ) -> Tuple[bool, List]:
        """
        Lets Riders out of the Elevator, and adds a delay if anyone does.

        Also removes the current Floor from both external and
        internal destinations.
        """
        riders_to_remove = []
        rider_names_to_remove = []
        should_door_open = False
        if self.floor in self.external_destinations:  # TODO: see if we need this
            self.external_destinations.remove(self.floor)
        if self.floor in self.internal_destinations:
            self.internal_destinations.remove(self.floor)  # ding, we stop
            for rider in self.riders:  # can we DRY?
                if rider.destination == self.floor:
                    riders_to_remove.append(rider)
                    rider_names_to_remove.append(str(rider))
                    rider_list.remove(rider)
                    rider.step_out(self, start_stop_delays, start_step_delays)
                    should_door_open = True
        for rider in riders_to_remove:
            self.riders.remove(rider)
        return should_door_open, rider_names_to_remove

    def update_direction_new(self, floor_dict) -> None:
        keep_going_down = False
        keep_going_up = False
        if self.internal_destinations:
            pass
        else:
            for floor in floor_dict.values():
                if isinstance(
                    floor, Floor
                ):  # there is a value in the floor_dict that is not a Floor but rather a Boolean
                    if keep_going_down and keep_going_up:
                        break
                    if floor.number > self.floor and (
                        floor.up_request or floor.down_request
                    ):
                        keep_going_up = True
                    elif floor.number < self.floor and (
                        floor.up_request or floor.down_request
                    ):
                        keep_going_down = True
                    elif floor.number == self.floor and (
                        self.direction > -1 and floor.up_request
                    ):
                        keep_going_up = True
                    elif floor.number == self.floor and (
                        self.direction < 1 and floor.down_request
                    ):
                        keep_going_down = True
                    else:
                        continue

            if (keep_going_down and self.direction == -1) or (
                keep_going_up and self.direction == 1
            ):
                pass
            elif (keep_going_down and self.direction == 1) or (
                keep_going_up and self.direction == -1
            ):
                self.direction = self.direction * -1
            elif self.direction == 0 and keep_going_down:
                self.direction = -1
            elif (
                self.direction == 0 and keep_going_up
            ):  # would these two lines imply that keep_going_up has priority?
                self.direction = 1
            else:
                self.direction = 0

    def update_direction_new_floor(self, e_bank: ElevatorBank) -> None:
        if self.direction == 0:
            if e_bank.queue:
                print("went to elev queue")
                next_floor = self.find_nearest_floor(list(e_bank.queue))
                if next_floor > self.floor:
                    self.direction = 1
                    self.external_destinations.add(next_floor)
                elif next_floor < self.floor:
                    self.direction = -1
                    self.external_destinations.add(next_floor)
                try:
                    e_bank.queue.remove(next_floor)
                except KeyError:
                    pass
        elif self.internal_destinations or self.external_destinations:
            pass
        else:
            self.direction = 0

    def let_riders_in_new(self, floor_dict, e_bank) -> None:
        clear_up_button = False
        clear_down_button = False
        riders_still_waiting = False
        should_door_open = False
        riders_to_step_in = []
        rider_names_to_add = []
        for rider in floor_dict[self.floor].riders:
            if self.direction == 1 and rider.destination > self.floor:  # going up
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    clear_up_button = True
                else:
                    riders_still_waiting = True
                should_door_open = True
            elif self.direction == -1 and rider.destination < self.floor:  # going down
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    clear_down_button = True
                else:
                    riders_still_waiting = True
                should_door_open = True
            else:
                pass
        # remove Rider from Floor if they are going in Elevator
        floor_dict[self.floor].riders = [
            e for e in floor_dict[self.floor].riders if e not in riders_to_step_in
        ]
        if not riders_still_waiting:
            if clear_up_button:
                floor_dict[self.floor].up_request = False
            if clear_down_button:
                floor_dict[self.floor].down_request = False
        return should_door_open, rider_names_to_add

    def let_riders_in_new_floor(self, floor_dict, e_bank) -> None:
        should_door_open = False
        riders_to_step_in = []
        rider_names_to_add = []

        for rider in floor_dict[self.floor].riders:
            if self.direction > -1 and rider.destination > self.floor:  # going up
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    should_door_open = True
                    try:
                        e_bank.queue.remove(self.floor)
                    except KeyError:
                        pass
                    self.direction = 1
                else:
                    rider.press_button_new_floor(e_bank)
            elif self.direction < 1 and rider.destination < self.floor:  # going down
                if rider.step_in(self):
                    rider_names_to_add.append(str(rider))
                    self.internal_destinations.add(rider.destination)
                    riders_to_step_in.append(rider)
                    should_door_open = True
                    try:
                        e_bank.queue.remove(self.floor)
                    except KeyError:
                        pass
                    self.direction = -1
                else:
                    rider.press_button_new_floor(e_bank)
            else:  # if there's an Elevator at our Floor but not in right direction
                rider.press_button_new_floor(e_bank)

        # remove Riders from Floor if they are going in Elevator
        floor_dict[self.floor].riders = [
            e for e in floor_dict[self.floor].riders if e not in riders_to_step_in
        ]
        return should_door_open, rider_names_to_add

    def find_nearest_floor(self, queue) -> int:
        if queue == None:
            return self.floor
        nearest_floor = maxsize
        for floor in queue:
            if abs(floor - self.floor) < abs(nearest_floor - self.floor):
                nearest_floor = floor
        return nearest_floor

    def destination_check(self, floor_dict) -> None:
        """
        Performs a sanity check on external destinations. If there is no Rider
        at a Floor that is an external destination,
        remove it from the list of external destinations.
        """
        ext_dests_copy = self.external_destinations.copy()
        for floor in ext_dests_copy:
            if not floor_dict[floor].riders:
                self.external_destinations.remove(floor)


# see http://www.facilitiesnet.com/elevators/article/Destination-Dispatch-Machineroomless-Systems-Are-Current-Wave-of-Elevator-Technology--13595?source=previous
# and https://www.thyssenkruppelevator.com/elevator-products/elevator-destination-dispatch


class Rider:
    def __init__(self, name, destination, start_floor):
        self.name = name
        self.destination = destination
        self.start_floor = start_floor
        self.curr_floor = start_floor
        self.when_to_add = 0
        self.step_in_time = 0
        self.is_in_elevator = False
        self.button_pressed = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} began on {self.start_floor}, is now on {self.curr_floor} and wants to go to {self.destination}"

    def step_in(self, elev) -> bool:
        if elev.capacity == len(elev.riders):
            print(f"Rider {self.name} can't enter elevator since it is full")
            return False
        else:
            self.step_in_time = elev.simulated_time
            self.is_in_elevator = True
            elev.riders.append(self)
            return True

    def step_out(self, elevator, start_stop_delays, start_step_delays) -> None:
        start_stop_delays.append(elevator.simulated_time - self.when_to_add)
        start_step_delays.append(self.step_in_time - self.when_to_add)

    def press_button_new(self, floor_dict) -> None:
        self.button_pressed = True
        if self.start_floor < self.destination:
            floor_dict[self.start_floor].up_request = True
        else:
            floor_dict[self.start_floor].down_request = True

    def press_button_new_floor(self, e_bank: ElevatorBank) -> None:
        nearest_elevator = self.find_nearest_available_elevator(e_bank)
        if nearest_elevator:
            nearest_elevator.external_destinations.add(self.start_floor)
            self.dispatched_elevator = nearest_elevator

    def find_nearest_available_elevator(self, elevator_bank: ElevatorBank) -> Elevator:
        """
        Returns the Elevator object that is the nearest (in terms of Floors)
        elevator that can pick up a rider. Elevator will probably be stationary,
        but can also return an Elevator that is on its way to the Rider's Floor,
        meaning has the proper direction and has a destination past the Rider's
        floor.

        If two elevators are equidistant then the higher elevator
        gets preference.

        Used for an elevator bank.
        """
        available_elevators = []
        for e in elevator_bank.elevators:
            # if e.direction == 0:
            #     available_elevators.append(e)
            if (
                self.destination > self.start_floor
                and (e.direction == 1)  # elevator going up
                and (e.floor < self.start_floor)
            ):
                available_elevators.append(e)
            elif (
                self.destination < self.start_floor
                and (e.direction == -1)  # elevator going down
                and (e.floor > self.start_floor)
            ):
                available_elevators.append(e)

        if not available_elevators:
            elevator_bank.queue.add(self.start_floor)
            return

        min_distance = abs(
            min(
                available_elevators, key=lambda x: abs(x.floor - self.start_floor)
            ).floor
            - self.start_floor
        )
        for e in available_elevators:  # higher elevators win tiebreaker
            if e.floor - self.start_floor == min_distance:
                return e
        for e in available_elevators:
            if self.start_floor - e.floor == min_distance:
                return e


class Floor:
    def __init__(self, number: int):
        self.number = number  # is this necessary if we have a dict of floors?
        self.riders = []
        self.has_elevator = False
        self.up_request = False
        self.down_request = False

    def __repr__(self):
        return f"Floor {self.number} has riders {[str(rider) for rider in self.riders]} and has {self.up_request} up request and {self.down_request} down request"
