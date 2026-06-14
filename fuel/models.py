from django.db import models

# Create your models here.

class FuelStation(models.Model):
    opis_truckstop_id = models.IntegerField(unique=True)
    truckstop_name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


class FuelPrice(models.Model):

    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE, related_name="prices")

    retail_price = models.DecimalField(max_digits=6, decimal_places=3)

    rack_id = models.IntegerField()





    