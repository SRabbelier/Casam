from django.db import models

class Patient(models.Model):
  corpse_id = models.IntegerField()
  sex = models.BooleanField()

class Image(models.Model):
  path = models.CharField(max_length=100)
  name = models.CharField(max_length=30)
  added = models.DateField(auto_now_add=True)
  last_modified = models.DateField(auto_now=True)
  is_left = models.BooleanField()

class OriginalImage(Image):
  patient = models.ForeignKey(Patient)

class WarpedImage(Image):
  pass
