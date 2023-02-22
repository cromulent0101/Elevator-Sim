# code taken from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# pylint: disable=import-error

from rest_framework import serializers
from .models import Simulation, SimulationRequest


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ("step_delays", "stop_delays", "floors_traversed", "log_dict")

    # run some custom code when an object comes in and gets created
    def create(self, validated_data):
        # items_data = validated_data.pop('items')

        # similar to Parent.objects.create(**validated_data)
        sim = Simulation.objects.create(
            step_delays="asdf",
            stop_delays="ASDASDASDASD",
            floors_traversed=2010201,
            log_dict="hello",
        )
        # parent = super().create(**validated_data)

        return sim


class SimulationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationRequest
        fields = ("rider_list", "num_elevators", "TIME_STEP", "elevate_type")
