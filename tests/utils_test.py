# pylint: disable=import-error
import pytest, utils
from classes import Elevator, Rider, ElevatorBank
from typing import List


@pytest.fixture
def classic_riders():
    return [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 1, 9)]


@pytest.fixture
def elevator_bank_mixed():
    el1 = Elevator(3, 10, "a")
    el1.direction = -1
    el2 = Elevator(3, 6, "b")
    el2.direction = -1
    el3 = Elevator(3, 4, "c")
    el3.direction = 0
    el4 = Elevator(3, 4, "d")
    el4.direction = -1
    el5 = Elevator(3, 1, "e")
    el5.direction = 1
    return ElevatorBank([el1, el2, el3, el4, el5])


@pytest.fixture
def elevator_bank_down():
    el1 = Elevator(3, 7, "a")
    el1.direction = -1
    el2 = Elevator(3, 6, "b")
    el2.direction = -1
    el3 = Elevator(3, 4, "c")
    el3.direction = -1
    el4 = Elevator(3, 4, "d")
    el4.direction = -1
    el5 = Elevator(3, 1, "e")
    el5.direction = -1
    return ElevatorBank([el1, el2, el3, el4, el5])


@pytest.fixture
def down_rider_9():
    return Rider("Joe", 2, 9)


@pytest.fixture
def down_rider_5():
    return Rider("Joe", 2, 5)


@pytest.fixture
def csv_file_classic() -> str:
    return "sims/classic.csv"


@pytest.fixture
def csv_file_empty() -> str:
    return "sims/empty.csv"


def test_find_nearest_elevator(down_rider_9: Rider, elevator_bank_mixed: ElevatorBank):
    el1 = Elevator(3, 10, "name")
    el1.direction = -1
    assert el1 == down_rider_9.find_nearest_available_elevator(elevator_bank_mixed)


def test_find_nearest_elevator_tie(
    down_rider_5: Rider, elevator_bank_mixed: ElevatorBank
):
    el2 = Elevator(3, 6, "name")
    el2.direction = -1
    assert el2 == down_rider_5.find_nearest_available_elevator(elevator_bank_mixed)


def test_find_nearest_elevator_none(
    down_rider_9: Rider, elevator_bank_down: ElevatorBank
):
    elev = down_rider_9.find_nearest_available_elevator(elevator_bank_down)
    print(elevator_bank_down.queue)
    assert None == elev
    assert down_rider_9.start_floor == elevator_bank_down.queue.pop()


def test_csv_import(
    csv_file_classic: str, classic_riders: List["Rider"]
):  # pass in a CSV with 3 riders and ensure 3 get created
    for i in range(len(classic_riders)):  # TODO: optimize this
        assert repr(utils.get_riders_from_csv(csv_file_classic)[i]) == repr(
            classic_riders[i]
        )
        # classic_riders


def test_empty_csv_import(
    csv_file_empty,
):  # pass in a CSV with just headers and make sure no riders get created but also not error
    assert len(utils.get_riders_from_csv(csv_file_empty)) == 0
