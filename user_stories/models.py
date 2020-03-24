from django.db import models
from django.utils.datetime_safe import datetime


# Create your models here.


class Sale(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    projector = models.BooleanField()

    @property
    def is_unavailable_today(self):
        today = datetime.today()
        return self.is_unavailable(today)


    def is_unavailable(self, date):
        response = self.reserv.filter(date=date).exists()
        return response

    def __str__(self):
        return self.name


class Reservation(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='reserv')
    date = models.DateField()
    comment = models.TextField(null=True)

