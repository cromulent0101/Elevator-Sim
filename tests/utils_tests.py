# pylint: disable=import-error
import pytest, utils
from classes import Elevator, Rider, ElevatorBank


@pytest.fixture
def elevator_bank_mixed():
    el1 = Elevator(3, 10)
    el1.direction = -1
    el2 = Elevator(3, 6)
    el2.direction = -1
    el3 = Elevator(3, 4)
    el3.direction = 0
    el4 = Elevator(3, 4)
    el4.direction = -1
    el5 = Elevator(3, 1)
    el5.direction = 1
    return ElevatorBank([el1, el2, el3, el4, el5])


@pytest.fixture
def elevator_bank_down():
    el1 = Elevator(3, 7)
    el1.direction = -1
    el2 = Elevator(3, 6)
    el2.direction = -1
    el3 = Elevator(3, 4)
    el3.direction = -1
    el4 = Elevator(3, 4)
    el4.direction = -1
    el5 = Elevator(3, 1)
    el5.direction = -1
    return ElevatorBank([el1, el2, el3, el4, el5])


@pytest.fixture
def down_rider_9():
    return Rider("Joe", 2, 9)


@pytest.fixture
def down_rider_5():
    return Rider("Joe", 2, 5)


def test_find_nearest_elevator(down_rider_9, elevator_bank_mixed):
    el1 = Elevator(3, 10)
    el1.direction = -1
    assert el1 == down_rider_9.find_nearest_available_elevator(elevator_bank_mixed)


def test_find_nearest_elevator_tie(down_rider_5, elevator_bank_mixed):
    el2 = Elevator(3, 6)
    el2.direction = -1
    assert el2 == down_rider_5.find_nearest_available_elevator(elevator_bank_mixed)


def test_find_nearest_elevator_none(down_rider_9, elevator_bank_down):
    elev = down_rider_9.find_nearest_available_elevator(elevator_bank_down)
    assert None == elev
    assert down_rider_9.start_floor == elevator_bank_down.queue.get()
