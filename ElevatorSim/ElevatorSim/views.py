# code from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# pylint: disable=import-error,no-member

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SimulationSerializer, SimulationRequestSerializer
from .models import Simulation, SimulationRequest

# Create your views here.


class SimulationView(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()


class SimulationRequestView(viewsets.ModelViewSet):
    serializer_class = SimulationRequestSerializer
    queryset = SimulationRequest.objects.all()
