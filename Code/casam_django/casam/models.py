from django.db import models

from django_tools import fields

class Patient(models.Model):
  id = fields.UUIDField(primary_key=True)
  corpse_id = models.IntegerField()
  sex = models.BooleanField()

class Image(models.Model):
  id = fields.UUIDField(primary_key=True)
  path = models.CharField(max_length=100)
  name = models.CharField(max_length=30)
  added = models.DateField(auto_now_add=True)
  last_modified = models.DateField(auto_now=True)
  is_left = models.BooleanField()

class OriginalImage(Image):
  patient = models.ForeignKey(Patient)

class WarpedImage(Image):
  pass
