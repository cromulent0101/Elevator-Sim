# pylint: disable=import-error
import pytest, utils
from classes import Elevator, Rider, ElevatorBank

# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data


@pytest.fixture
def first_floor_elevator():
    return Elevator(3, 1)


@pytest.fixture
def middle_floor_elevator():
    return Elevator(3, 3)


@pytest.fixture
def top_floor_elevator():
    return Elevator(3, 12)


@pytest.fixture
def classic_riders():
    return utils.get_riders_from_csv("sims/classic.csv")


@pytest.fixture
def edge_cases_riders():
    return utils.get_riders_from_csv("sims/edge_cases.csv")


@pytest.fixture
def edge_case_1_riders():
    return utils.get_riders_from_csv("sims/edge_case_1.csv")


def test_first_classic(first_floor_elevator, classic_riders):
    e_bank = [first_floor_elevator]
    bank = ElevatorBank(e_bank)
    floor_dict = utils.create_floors(classic_riders, e_bank, bank)

    start_step_delays, start_stop_delays, log_dict = bank.simulate(
        classic_riders, floor_dict
    )


# def test_first_descending(first_floor_elevator, descending_riders):
#     floor_dict = utils.create_floors(descending_riders)
#     assert first_floor_elevator.run(descending_riders, floor_dict) == [
#         "1;1;;",
#         "2;1;;",
#         "3;1;;",
#         "4;1;;",
#         "5;1;;",
#         "6;1;;",
#         "7;1;;",
#         "8;1;;",
#         "9;1;Joe;",
#         "8;-1;;",
#         "7;-1;Jane;",
#         "6;-1;;",
#         "5;-1;Bob;",
#         "4;-1;;Bob",
#         "3;-1;;Jane",
#         "2;-1;;Joe",
#     ]


# def test_middle_classic(middle_floor_elevator, classic_riders):
#     floor_dict = utils.create_floors(classic_riders)
#     assert middle_floor_elevator.run(classic_riders, floor_dict) == [
#         "3;1;;",
#         "4;1;Bob;",
#         "5;1;;Bob",
#         "6;1;;",
#         "7;1;;",
#         "8;1;;",
#         "9;1;Jane;",
#         "8;-1;;",
#         "7;-1;;",
#         "6;-1;;",
#         "5;-1;;",
#         "4;-1;;",
#         "3;-1;;",
#         "2;-1;;",
#         "1;-1;;Jane",
#         "2;1;Joe;",
#         "3;1;;",
#         "4;1;;",
#         "5;1;;",
#         "6;1;;",
#         "7;1;;",
#         "8;1;;",
#         "9;1;;Joe",
#     ]


# def test_middle_multiple(middle_floor_elevator, multiple_riders_multiple_floors):
#     floor_dict = utils.create_floors(multiple_riders_multiple_floors)
#     assert middle_floor_elevator.run(multiple_riders_multiple_floors, floor_dict) == [
#         "3;1;;",
#         "4;1;;",
#         "5;1;Jill;",
#         "6;1;;",
#         "7;1;;",
#         "8;1;;",
#         "9;1;Jimmy,Joe;Jill",
#         "8;-1;;",
#         "7;-1;;",
#         "6;-1;;",
#         "5;-1;Bob,Jane;Jimmy",
#         "4;-1;;",
#         "3;-1;;Jane",
#         "2;-1;;Bob,Joe",
#     ]


# def test_middle_stationary_up():  # stationary elevator with
#     pass
