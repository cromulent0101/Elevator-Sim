# pylint: disable=import-error
# pylint: disable=wrong-import-position
from typing import List
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
    SIM_TYPE = "elevate_normal"
    return [TIME_STEP, MAX_TIME, SIM_TYPE]


@pytest.fixture
def simulation_settings_dispatch():
    TIME_STEP = 0.01
    MAX_TIME = 10000
    SIM_TYPE = "elevate_normal"
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


def test_first_middle_classic(
    first_floor_elevator: Elevator,
    middle_floor_elevator: Elevator,
    classic_riders: List[Rider],
    simulation_settings_normal: list,
):

    classic_riders_copy = classic_riders.copy()
    e_bank = [first_floor_elevator, middle_floor_elevator]
    bank = ElevatorBank(e_bank)
    floor_dict = utils.create_floors(classic_riders, e_bank)

    _, _, _, log_dict = bank.simulate(
        classic_riders,
        floor_dict,
        simulation_settings_normal[0],
        simulation_settings_normal[1],
        simulation_settings_normal[2],
    )

    # loop through each Elevator's log_dict and see if the first Rider gets on and gets off
    rider_went_in = []
    for log in log_dict.values():
        if "".join(list(log)).count(classic_riders_copy[0].name) == 2:
            rider_went_in.append(True)
        else:
            rider_went_in.append(False)

    assert rider_went_in.count(True) == 1
    # Counts that the first Rider got on and also got off.
    # assumes Rider names are prefix-free
