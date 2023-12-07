from django.db import models
import uuid
from django.conf import settings

class User_Details(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    occupation = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    maritalStatus = models.CharField(max_length=20)
    race = models.CharField(max_length=20)
    education = models.CharField(max_length=20)

    fingerprint_name = models.BigIntegerField(null=True,blank=True)
    fingerprint_age = models.BigIntegerField(null=True,blank=True)
    # fingerprint_occupation = models.BigIntegerField(null=True,blank=True)
    # fingerprint_sex = models.BigIntegerField(null=True,blank=True)
    # fingerprint_maritalStatus = models.BigIntegerField(null=True,blank=True)
    # fingerprint_race = models.BigIntegerField(null=True,blank=True)
    # fingerprint_education = models.BigIntegerField(null=True,blank=True)
    