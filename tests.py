# pylint: disable=import-error
import pytest
from classes import InefficientElevator, Rider

# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data


@pytest.fixture
def first_floor_elevator():
    e = InefficientElevator(3, 1)
    e.direction = 1
    return e


@pytest.fixture
def middle_floor_elevator():
    e = InefficientElevator(3, 5)
    e.direction = 1
    return e


@pytest.fixture
def classic_riders():
    return [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 1, 9)]


@pytest.fixture
def ascending_riders():
    return [Rider("Joe", 9, 2), Rider("Bob", 5, 4), Rider("Jane", 7, 3)]


@pytest.fixture
def descending_riders():
    return [Rider("Joe", 2, 9), Rider("Bob", 4, 5), Rider("Jane", 3, 7)]


def test_first_classic(first_floor_elevator, classic_riders):
    for rider in classic_riders:
        first_floor_elevator.destinations.add(rider.start_floor)
    assert first_floor_elevator.run(classic_riders) == [
        "1;1;;",
        "2;1;Joe;",
        "3;1;;",
        "4;1;Bob;",
        "5;1;;Bob",
        "6;1;;",
        "7;1;;",
        "8;1;;",
        "9;1;Jane;Joe",
        "8;-1;;",
        "7;-1;;",
        "6;-1;;",
        "5;-1;;",
        "4;-1;;",
        "3;-1;;",
        "2;-1;;",
        "1;-1;;Jane",
    ]


def test_first_descending(first_floor_elevator, descending_riders):
    for rider in descending_riders:
        first_floor_elevator.destinations.add(rider.start_floor)
    assert first_floor_elevator.run(descending_riders) == [
        "1;1;;",
        "2;1;;",
        "3;1;;",
        "4;1;;",
        "5;1;;",
        "6;1;;",
        "7;1;;",
        "8;1;;",
        "9;1;Joe;",
        "8;-1;;",
        "7;-1;Jane;",
        "6;-1;;",
        "5;-1;Bob;",
        "4;-1;;Bob",
        "3;-1;;Jane",
        "2;-1;;Joe",
    ]
