# pylint: disable=import-error
import pytest, utils
from classes import Elevator, Rider, ElevatorBank

# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data


@pytest.fixture
def first_floor_elevator():
    e = Elevator(3, 1, "first_floor_elevator")
    e.direction = 1
    return e


@pytest.fixture
def middle_floor_elevator():
    e = Elevator(3, 3, "middle_floor_elevator")
    e.direction = 1
    return e


@pytest.fixture
def top_floor_elevator():
    e = Elevator(3, 12, "top_floor_elevator")
    e.direction = -1
    return e


@pytest.fixture
def middle_floor_stationary_elevator():
    e = Elevator(3, 3, "middle_floor_elevator_stationary")
    e.direction = 0
    return e


@pytest.fixture
def classic_riders():
    return [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 1, 8)]


@pytest.fixture
def ascending_riders():
    return [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 7, 3)]


@pytest.fixture
def descending_riders():
    return [Rider("Joe", 2, 9), Rider("Bob", 4, 5), Rider("Jane", 3, 7)]


@pytest.fixture
def multiple_riders_multiple_floors():
    return [
        Rider("Joe", 2, 9),
        Rider("Bob", 2, 5),
        Rider("Jane", 3, 5),
        Rider("Jimmy", 5, 9),
        Rider("Jill", 9, 5),
    ]


def test_first_classic_dc(first_floor_elevator, classic_riders):
    classic_riders_copy = classic_riders.copy()
    floor_dict = utils.create_floors(classic_riders, [first_floor_elevator])
    elevator_bank = ElevatorBank([first_floor_elevator])
    _, _, _, log_dict = elevator_bank.simulate(
        classic_riders, floor_dict, 0.5, 10000, "elevate_dc"
    )
    assert (
        "".join(list(log_dict.values())[0]).count(classic_riders_copy[0].name) == 2
    )  # Counts that the first Rider got on and also got off.
    assert log_dict[f"Elevator {first_floor_elevator.name}"] == [
        "1;1;;;0",
        "2;1;Joe;;0.5",
        "3;1;;;2.0",
        "4;1;Bob;;2.5",
        "5;1;;Bob;4.0",  # If we change Jane to be on Floor 8, this becomes an issue as Floor 5 appears twice when it shouldn't!
        "6;1;;;5.5",
        "7;1;;;6.0",
        "8;1;;;6.5",
        "9;-1;Jane;Joe;7.0",
        "8;-1;;;8.5",
        "7;-1;;;9.0",
        "6;-1;;;9.5",
        "5;-1;;;10.0",
        "4;-1;;;10.5",
        "3;-1;;;11.0",
        "2;-1;;;11.5",
        "1;0;;Jane;12.0",
        "1;0;;;13.5",
    ]


def test_first_descending_dc(first_floor_elevator, descending_riders):
    descending_riders_copy = descending_riders.copy()
    floor_dict = utils.create_floors(descending_riders, [first_floor_elevator])
    elevator_bank = ElevatorBank([first_floor_elevator])
    _, _, _, log_dict = elevator_bank.simulate(
        descending_riders, floor_dict, 0.5, 10000, "elevate_dc"
    )
    assert (
        "".join(list(log_dict.values())[0]).count(descending_riders_copy[0].name) == 2
    )  # Counts that the first Rider got on and also got off.
    assert log_dict[f"Elevator {first_floor_elevator.name}"] == [
        "1;1;;;0",
        "2;1;;;0.5",
        "3;1;;;1.0",
        "4;1;;;1.5",
        "5;1;;;2.0",
        "6;1;;;2.5",
        "7;1;;;3.0",
        "8;1;;;3.5",
        "9;-1;Joe;;4.0",
        "8;-1;;;5.5",
        "7;-1;Jane;;6.0",
        "6;-1;;;7.5",
        "5;-1;Bob;;8.0",
        "4;-1;;Bob;9.5",
        "3;-1;;Jane;11.0",
        "2;0;;Joe;12.5",
        "2;0;;;14.0",
    ]


def test_middle_classic_dc(middle_floor_elevator, classic_riders):
    floor_dict = utils.create_floors(classic_riders, [middle_floor_elevator])
    elevator_bank = ElevatorBank([middle_floor_elevator])
    _, _, _, log_dict = elevator_bank.simulate(
        classic_riders, floor_dict, 0.5, 10000, "elevate_dc"
    )
    assert log_dict[f"Elevator {middle_floor_elevator.name}"] == [
        "3;1;;;0",
        "4;1;Bob;;0.5",
        "5;0;;Bob;2.0",  # goes to elev queue here
        "5;-1;;;3.5",
        "4;-1;;;4.0",
        "3;-1;;;4.5",
        "2;1;Joe;;5.0",
        "3;1;;;6.5",
        "4;1;;;7.0",
        "5;1;;;7.5",
        "6;1;;;8.0",
        "7;1;;;8.5",
        "8;1;;;9.0",
        "9;-1;Jane;Joe;9.5",
        "8;-1;;;11.0",
        "7;-1;;;11.5",
        "6;-1;;;12.0",
        "5;-1;;;12.5",
        "4;-1;;;13.0",
        "3;-1;;;13.5",
        "2;-1;;;14.0",
        "1;0;;Jane;14.5",
        "1;0;;;16.0",
    ]


def test_middle_multiple_dc(middle_floor_elevator, multiple_riders_multiple_floors):
    floor_dict = utils.create_floors(
        multiple_riders_multiple_floors, [middle_floor_elevator]
    )
    elevator_bank = ElevatorBank([middle_floor_elevator])
    _, _, _, log_dict = elevator_bank.simulate(
        multiple_riders_multiple_floors, floor_dict, 0.5, 10000, "elevate_dc"
    )
    assert log_dict[f"Elevator {middle_floor_elevator.name}"] == [
        "3;1;;;0",
        "4;1;;;0.5",
        "5;1;Jill;;1.0",
        "6;1;;;2.5",
        "7;1;;;3.0",
        "8;1;;;3.5",
        "9;-1;Jimmy,Joe;Jill;4.0",
        "8;-1;;;5.5",
        "7;-1;;;6.0",
        "6;-1;;;6.5",
        "5;-1;Bob,Jane;Jimmy;7.0",
        "4;-1;;;8.5",
        "3;-1;;Jane;9.0",
        "2;0;;Bob,Joe;10.5",
        "2;0;;;12.0",
    ]


# stationary elevator with Riders equidistant above and below. should prefer going down first
def test_middle_stationary_dc(middle_floor_stationary_elevator, classic_riders):
    classic_riders_copy = classic_riders.copy()
    floor_dict = utils.create_floors(classic_riders, [middle_floor_stationary_elevator])
    elevator_bank = ElevatorBank([middle_floor_stationary_elevator])
    _, _, _, log_dict = elevator_bank.simulate(
        classic_riders, floor_dict, 0.5, 10000, "elevate_dc"
    )
    assert (
        "".join(list(log_dict.values())[0]).count(classic_riders_copy[0].name) == 2
    )  # Counts that the first Rider got on and also got off.
    assert log_dict[f"Elevator {middle_floor_stationary_elevator.name}"] == [
        "3;-1;;;0",
        "2;1;Joe;;0.5",
        "3;1;;;2.0",
        "4;1;Bob;;2.5",
        "5;1;;Bob;4.0",
        "6;1;;;5.5",
        "7;1;;;6.0",
        "8;1;;;6.5",
        "9;-1;Jane;Joe;7.0",
        "8;-1;;;8.5",
        "7;-1;;;9.0",
        "6;-1;;;9.5",
        "5;-1;;;10.0",
        "4;-1;;;10.5",
        "3;-1;;;11.0",
        "2;-1;;;11.5",
        "1;0;;Jane;12.0",
        "1;0;;;13.5",
    ]


def test_full_elevator():
    pass
