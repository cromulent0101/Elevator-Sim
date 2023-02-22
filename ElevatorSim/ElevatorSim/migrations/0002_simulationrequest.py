# Generated by Django 4.1.3 on 2023-02-16 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ElevatorSim", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimulationRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rider_list", models.CharField(max_length=5000)),
                ("num_elevators", models.IntegerField()),
                ("TIME_STEP", models.FloatField()),
                ("elevate_type", models.TextField()),
            ],
        ),
    ]
