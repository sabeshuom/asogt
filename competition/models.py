from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


# class Students(models.Model):
#     GENDER_OPTIONS = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('ND', 'Prefer not to disclose'),
#     )
#     userid = models.PositiveIntegerField()
#     firstname = models.CharField(max_length=200)
#     lastname = models.CharField(max_length=200)
#     firstname_tamil = models.CharField(max_length=200)
#     lastname_tamil = models.CharField(max_length=200)
#     gender = models.CharField(max_length=2, choices=GENDER_OPTIONS)
#     dob = models.DateField()
#     phone = models.CharField(max_length=15)
#     email = models.CharField(max_length=50)


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
