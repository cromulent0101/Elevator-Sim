# code taken from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# pylint: disable=import-error

from rest_framework import serializers
from .models import Simulation


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ("step_delays", "stop_delays", "floors_traversed", "log_dict")
