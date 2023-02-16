from django.db import models

# Create your models here.


class Simulation(models.Model):
    step_delays = models.TextField()
    stop_delays = models.TextField()
    floors_traversed = models.IntegerField()
    log_dict = models.TextField()


class SimulationRequest(models.Model):
    rider_list = models.CommaSeparatedIntegerField(max_length=5000)
    num_elevators = models.IntegerField()
    TIME_STEP = models.FloatField()
    elevate_type = models.TextField()
    # def _str_(self):
    #     return self.title
