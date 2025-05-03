from django.db import models
from django.contrib.auth import get_user_model

## these models are what ill use to store cars to the garage and store/update the checklist

User = get_user_model()

class CarsInGarage(models.Model):
    # will be used to store cars into the garage

    # user that stored the car to their garage along with the cars reg
    linkeduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='garage')
    regnum = models.CharField(max_length=10)

    class Meta: unique_together = ['linkeduser', 'regnum'] # means one reg per user can be stored

class SavedChecklist(models.Model):
    # will be used to store and upate the checklist for users

    # same principle the user that the checklist belongs to with the cars reg
    linkeduser = models.ForeignKey(User, on_delete=models.CASCADE)
    regnum = models.CharField(max_length=20)
    # this is the checklist, stored in json to allow a structured add and update format and easy
    #django to vue worklflow
    carchecklist = models.JSONField(default=dict)
