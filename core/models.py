from django.db import models


class Regi(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField()
    key = models.TextField()


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
