from django.db import models

# Create your models here.


class generatekey(models.Model):
    key = models.CharField(max_length=6)
    def __str__(self):
        return self.key


class Sep(models.Model):
    nomorsep = models.CharField(max_length=19,default="")
    nomorsuratkontrol = models.CharField(max_length=6,default="")
    def __str__(self):
        return self.nomorsuratkontrol