# code from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# pylint: disable=import-error

from django.contrib import admin
from .models import Simulation, SimulationRequest


class SimulationAdmin(admin.ModelAdmin):
    list_display = ("step_delays", "stop_delays", "floors_traversed", "log_dict")


class SimulationRequestAdmin(admin.ModelAdmin):
    list_display = ("rider_list", "num_elevators", "TIME_STEP", "elevate_type")


# Register your models here.

admin.site.register(Simulation, SimulationAdmin)
admin.site.register(SimulationRequest, SimulationRequestAdmin)
