# pylint: disable=import-error
# pylint: disable=wrong-import-position
import pytest
import sys

sys.path.append("..")
import utils
from classes import Elevator, Rider, ElevatorBank

# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data


@pytest.fixture
def simulation_settings_normal():
    TIME_STEP = 0.01
    MAX_TIME = 10000
    SIM_TYPE = "elevate"
    return [TIME_STEP, MAX_TIME, SIM_TYPE]


@pytest.fixture
def simulation_settings_dispatch():
    TIME_STEP = 0.01
    MAX_TIME = 10000
    SIM_TYPE = "elevate_floor"
    return [TIME_STEP, MAX_TIME, SIM_TYPE]


@pytest.fixture
def first_floor_elevator():
    return Elevator(3, 1, "first")


@pytest.fixture
def middle_floor_elevator():
    return Elevator(3, 3, "middle")


@pytest.fixture
def top_floor_elevator():
    return Elevator(3, 12, "top")


@pytest.fixture
def classic_riders():
    return utils.get_riders_from_csv("./sims/classic.csv")


@pytest.fixture
def edge_cases_riders():
    return utils.get_riders_from_csv("../sims/edge_cases.csv")


@pytest.fixture
def edge_case_1_riders():
    return utils.get_riders_from_csv("../sims/edge_case_1.csv")


@pytest.fixture
def random100_riders():
    return utils.get_riders_from_csv("../sims/100random.csv")


@pytest.fixture
def random100_at_once_riders():
    return utils.get_riders_from_csv("./sims/100random_at_once.csv")


# TODO: add actual assert statements here
def test_first_classic(
    first_floor_elevator, classic_riders, simulation_settings_normal
):
    e_bank = [first_floor_elevator]
    bank = ElevatorBank(e_bank)
    floor_dict = utils.create_floors(classic_riders, e_bank)

    start_step_delays, start_stop_delays, floors_traversed, log_dict = bank.simulate(
        classic_riders,
        floor_dict,
        simulation_settings_normal[0],
        simulation_settings_normal[1],
        simulation_settings_normal[2],
    )
    # print(classic_riders[0])
    # print(log_dict.values[0])
    # assert classic_riders[0].name in ''.join(log_dict.values[0])


def test_random100(
    first_floor_elevator, random100_at_once_riders, simulation_settings_normal
):
    e_bank = [first_floor_elevator]
    bank = ElevatorBank(e_bank)
    floor_dict = utils.create_floors(random100_at_once_riders, e_bank)

    start_step_delays, start_stop_delays, floors_traversed, log_dict = bank.simulate(
        random100_at_once_riders,
        floor_dict,
        simulation_settings_normal[0],
        simulation_settings_normal[1],
        simulation_settings_normal[2],
    )
