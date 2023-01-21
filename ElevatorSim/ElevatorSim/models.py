from django.db import models

# Create your models here.


class Simulation(models.Model):
    step_delays = models.TextField()
    stop_delays = models.TextField()
    floors_traversed = models.IntegerField()
    log_dict = models.TextField()

    # def _str_(self):
    #     return self.title
