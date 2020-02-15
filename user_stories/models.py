from django.db import models

# Create your models here.



class Sale(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    projector = models.BooleanField()


    def is_unavaliable(self, date):
       return self.reserv.filter(date=date).exst()



class Reservation(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='reserv')
    date = models.DateField()
    comment = models.TextField()
