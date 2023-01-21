# code from https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# pylint: disable=import-error

from django.contrib import admin
from .models import Simulation


class SimulationAdmin(admin.ModelAdmin):
    list_display = ("step_delays", "stop_delays", "floors_traversed", "log_dict")


# Register your models here.

admin.site.register(Simulation, SimulationAdmin)
