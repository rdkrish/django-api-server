from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Account(models.Model):
  auth_id = models.CharField(max_length=40)
  username = models.CharField(max_length=30)

  class Meta:
    app_label = 'api'
    db_table = 'account'

class PhoneNumber(models.Model):
  number = models.CharField(max_length=40)
  account = models.ForeignKey(Account, on_delete=models.CASCADE)

  class Meta:
    app_label = 'api'
    db_table = 'phone_number'
