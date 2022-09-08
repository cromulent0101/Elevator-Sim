# pylint: disable=import-error
import pytest, utils
from classes import InefficientElevator, Rider

# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data


@pytest.fixture
def first_floor_elevator():
    e = InefficientElevator(3, 1)
    e.direction = 1
    return e


@pytest.fixture
def middle_floor_elevator():
    e = InefficientElevator(3, 3)
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


# @pytest.fixure(autouse=True)
# def get_floors():
#     return


def test_first_classic(first_floor_elevator, classic_riders):
    floor_dict = utils.create_floors(classic_riders)
    assert first_floor_elevator.run(classic_riders, floor_dict) == [
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
    floor_dict = utils.create_floors(descending_riders)
    assert first_floor_elevator.run(descending_riders, floor_dict) == [
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


def test_middle_classic(middle_floor_elevator, classic_riders):
    floor_dict = utils.create_floors(classic_riders)
    assert middle_floor_elevator.run(classic_riders, floor_dict) == [
        "3;1;;",
        "4;1;Bob;",
        "5;1;;Bob",
        "6;1;;",
        "7;1;;",
        "8;1;;",
        "9;1;Jane;",
        "8;-1;;",
        "7;-1;;",
        "6;-1;;",
        "5;-1;;",
        "4;-1;;",
        "3;-1;;",
        "2;-1;;",
        "1;-1;;Jane",
        "2;1;Joe;",
        "3;1;;",
        "4;1;;",
        "5;1;;",
        "6;1;;",
        "7;1;;",
        "8;1;;",
        "9;1;;Joe",
    ]
