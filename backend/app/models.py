from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='vehicles')


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20, unique=True)


class Violation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='violations')
    timestamp = models.DateTimeField()
    comments = models.TextField()
    officer = models.ForeignKey(Officer, on_delete=models.SET_NULL, null=True)
