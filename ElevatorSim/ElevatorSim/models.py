from django.db import models

# Create your models here.


class Simulation(models.Model):
    id = models.IntegerField(primary_key=True)
    step_delays = models.TextField()
    stop_delays = models.TextField()
    floors_traversed = models.IntegerField()
    log_dict = models.TextField()
    rider_list = models.TextField()
    num_elevators = models.IntegerField()
    TIME_STEP = models.FloatField()
    elevate_type = models.TextField()


class SimulationRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    step_delays = models.TextField(blank=True, default="")
    stop_delays = models.TextField(blank=True, default="")
    floors_traversed = models.IntegerField(blank=True, default=1)
    log_dict = models.TextField(blank=True, default="")
    graph_id = models.IntegerField(blank=True, default=1)
    rider_list = models.TextField()
    num_elevators = models.IntegerField()
    TIME_STEP = models.FloatField()
    elevate_type = models.TextField()
