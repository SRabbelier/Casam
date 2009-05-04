from django.db import models

from django.contrib.auth.models import User

from django_extensions.db.fields import UUIDField


class Tag(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  name = models.CharField(max_length=50)

  def __unicode__(self):
    return str(self.name)


class Project(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  name = models.CharField(max_length=100)
  added = models.DateField(auto_now_add=True)
  description = models.CharField(max_length=200)
  tags = models.ManyToManyField('Tag', related_name='projects')

  def __unicode__(self):
    return str(self.name)


class Patient(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  corpse_id = models.IntegerField()
  sex = models.BooleanField()


class Image(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  project = models.ForeignKey('Project')
  path = models.CharField(max_length=100)
  name = models.CharField(max_length=30)
  added = models.DateField(auto_now_add=True)
  last_modified = models.DateField(auto_now=True)
  is_left = models.BooleanField()

  class Meta:
    abstract = True


class OriginalImage(Image):
  patient = models.ForeignKey('Patient')


class WarpedImage(Image):
  pass


class ProjectMeasurementList(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  project = models.ForeignKey('Project')
  name = models.CharField(max_length=30)


class Measurement(models.Model):
  id = UUIDField(primary_key=True,auto=True)
  project = models.ForeignKey('Project')
  mogelijkemeting = models.ForeignKey('ProjectMeasurementList')
  x = models.CharField(max_length=4)
  y = models.CharField(max_length=4)


class UserProfile(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  user = models.ForeignKey(User, unique=True)  
  read = models.ManyToManyField('Project', related_name='ReadProject')
  write = models.ManyToManyField('Project', related_name='WriteProject')


class Annotation(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  name = models.CharField(max_length=30)
  url = models.CharField(max_length=200)
  project = models.ForeignKey('Project')
