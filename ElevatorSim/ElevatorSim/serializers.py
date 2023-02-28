# code taken from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# see https://github.com/buckyroberts/Vataxia/tree/master/v1 for example DRF usage in general
# seee https://stackoverflow.com/questions/70492496/how-i-can-set-id-in-django-rest-framework-jsonapi-response for how to get ID back in response
# pylint: skip-file
import sys

sys.path.append("..")
import utils
from classes import Elevator, Rider, Floor, ElevatorBank
from rest_framework import serializers
from .models import Simulation, SimulationRequest


class SimulationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Simulation
        fields = ("id", "step_delays", "stop_delays", "floors_traversed", "log_dict")

    # run some custom code when an object comes in and gets created
    def create(self, validated_data):
        # items_data = validated_data.pop('items')

        # similar to Parent.objects.create(**validated_data)
        sim = Simulation.objects.create(
            id=123323123123123,
            step_delays="i am new",
            stop_delays="ASDASDASDASD",
            floors_traversed=2010201,
            log_dict="hello",
            TIME_STEP=0.5,
            rider_list="test",
            elevate_type="elevate",
            num_elevators=1,
        )
        # parent = super().create(**validated_data)

        return sim


class SimulationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationRequest
        fields = ("rider_list", "num_elevators", "TIME_STEP", "elevate_type")

    def create(self, validated_data):
        # hardcode 6 elevs for now with 3 capacity
        a = Elevator(3, 1, "a")
        b = Elevator(3, 1, "b")
        c = Elevator(3, 1, "c")
        d = Elevator(3, 1, "d")
        e = Elevator(3, 1, "e")
        f = Elevator(3, 1, "f")

        e_bank = [a, b, c, d, e, f]

        # this should be split out
        rider_list = []
        rider_input = validated_data.pop(
            "rider_list"
        )  # can we eventually push back to validated_data?
        for line in rider_input:
            rider_data = line.split(";")
            new_rider = Rider(rider_data[0], int(rider_data[1]), int(rider_data[2]))
            new_rider.when_to_add = int(rider_data[3])
            rider_list.append(new_rider)

        NUM_ELEVATORS = validated_data.pop("num_elevators")
        MAX_TIME = 10000
        bank = ElevatorBank(e_bank[:NUM_ELEVATORS])
        floor_dict = utils.create_floors(rider_list, e_bank[:NUM_ELEVATORS])

        (
            start_step_delays,
            start_stop_delays,
            floors_traversed,
            log_dict,
        ) = bank.simulate(
            rider_list,
            floor_dict,
            validated_data.pop("TIME_STEP"),
            MAX_TIME,
            validated_data.pop("elevate_type"),
        )

        sim = SimulationRequest.objects.create(
            rider_list="asdf",
            num_elevators="ASDASDASDASD",
            TIME_STEP=0.1,
            elevate_type="hello",
        )
        # parent = super().create(**validated_data)

        return sim
