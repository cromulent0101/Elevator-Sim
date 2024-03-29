# code taken from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# see https://github.com/buckyroberts/Vataxia/tree/master/v1 for example DRF usage in the wild
# seee https://stackoverflow.com/questions/70492496/how-i-can-set-id-in-django-rest-framework-jsonapi-response for how to get ID back in response
# for larger web app with AWS integration and authz look at https://www.reddit.com/r/django/comments/11f1w49/built_a_fullstack_blog_web_app_using/
# pylint: skip-file
import sys
import random

sys.path.append("..")
import utils
import graphs
from classes import Elevator, Rider, Floor, ElevatorBank
from rest_framework import serializers
from .models import Simulation, SimulationRequest


class SimulationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Simulation
        fields = ("id", "step_delays", "stop_delays", "floors_traversed", "log_dict")


class SimulationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationRequest
        fields = (
            "num_elevators",
            "TIME_STEP",
            "elevate_type",
            "rider_list",
            "graph_id",
            "step_delays",
            "stop_delays",
            "floors_traversed",
            "log_dict",
            "graph_id",
        )

    def create(self, validated_data):
        # hardcode 6 elevs for now with 3 capacity each
        # TODO: Make Elevators customizable
        a = Elevator(3, 1, "a")
        b = Elevator(3, 1, "b")
        c = Elevator(3, 1, "c")
        d = Elevator(3, 1, "d")
        e = Elevator(3, 1, "e")
        f = Elevator(3, 1, "f")

        e_bank = [a, b, c, d, e, f]

        # this should be split out
        rider_input = validated_data.pop(
            "rider_list"
        )  # can we eventually push back to validated_data?
        rider_list = utils.get_riders_from_string(rider_input)

        NUM_ELEVATORS = validated_data.pop("num_elevators")
        TIME_STEP = validated_data.pop("TIME_STEP")
        elevate_type = validated_data.pop("elevate_type")
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
            TIME_STEP,
            MAX_TIME,
            elevate_type,
        )
        graph_id = graphs.generate_histogram(start_step_delays)

        sim = SimulationRequest.objects.create(
            id=random.randint(0, 10000),
            step_delays=start_step_delays,
            stop_delays=start_stop_delays,
            floors_traversed=floors_traversed,
            log_dict=log_dict,
            graph_id=graph_id,
            TIME_STEP=TIME_STEP,
            rider_list=rider_input,
            elevate_type=elevate_type,
            num_elevators=NUM_ELEVATORS,
        )
        # parent = super().create(**validated_data)
        return sim
