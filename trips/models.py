from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class TravelPlan(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    days = models.IntegerField()
    weather_forecast = models.TextField()
    plan_details = models.TextField()

    def __str__(self):
        return f"{self.destination.name} - {self.days} days"
