# pylint: disable=import-error
import pytest
from classes import Elevator,Rider
# https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data

@pytest.fixture
def first_floor_elevator():
    return Elevator(3,1)