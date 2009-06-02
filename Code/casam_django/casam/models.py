from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

class Tag(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  name = models.CharField(max_length=50)

  def __unicode__(self):
    return str(self.name)


class Project(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  name = models.CharField(max_length=100)
  added = models.DateField(auto_now_add=True)
  description = models.CharField(max_length=200)
  tags = models.ManyToManyField('Tag', related_name='projects')

  def __unicode__(self):
    return str(self.name)


class Image(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  project = models.ForeignKey('Project')
  name = models.CharField(max_length=30)
  added = models.DateField(auto_now_add=True)
  last_modified = models.DateField(auto_now=True)

  def __unicode__(self):
    return str(self.name)

  class Meta:
    abstract = True
    
class PDM(Image):
  pass


class OriginalImage(Image):
  def __unicode__(self):
    return str(self.name)

class ModifiedImage(Image):
  originalimage = models.ForeignKey('OriginalImage') 
  hash = models.CharField(max_length=40) 
  transformation = models.TextField() 
  def __unicode__(self):
    return str(self.name)

class PotentialMeasurement(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  project = models.ForeignKey('Project')
  name = models.CharField(max_length=30)
  type = models.ForeignKey('PotentialMeasurementType')
  soort = models.CharField(max_length=1)
  def __unicode__(self):
    return str(self.name)

class Measurement(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  image = models.ForeignKey('OriginalImage')
  mogelijkemeting = models.ForeignKey('PotentialMeasurement')
  x = models.CharField(max_length=4)
  y = models.CharField(max_length=4)
  imagewidth = models.CharField(max_length=4)
  imageheight = models.CharField(max_length=4)
  def type(self):
    return self.mogelijkemeting.type
  def project(self):
    return self.image.project
  def __unicode__(self):
    return str(self.mogelijkemeting.name)
  

class Bitmap(Image):
  image = models.ForeignKey('OriginalImage')
  mogelijkemeting = models.ForeignKey('PotentialMeasurement')
  imagewidth = models.CharField(max_length=4)
  imageheight = models.CharField(max_length=4)
  minx = models.CharField(max_length=4)
  maxx = models.CharField(max_length=4)
  miny = models.CharField(max_length=4)
  maxy = models.CharField(max_length=4)
  path = models.CharField(max_length=200)
  def type(self):
    return self.mogelijkemeting.type
  def project(self):
    return self.image.project
  

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
  
class PotentialMeasurementType(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  name = models.CharField(max_length=40)
  project = models.ForeignKey('Project')
  
  def __unicode__(self):
    return str(self.name)
    
class State(models.Model):
  id = UUIDField(primary_key=True, auto=True)
  name = models.CharField(max_length=30)
  serializedState = models.TextField()
  width = models.IntegerField()
  height = models.IntegerField()
  project = models.ForeignKey('Project')
  added = models.DateField(auto_now_add=True)

