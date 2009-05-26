import sys
import os
import itertools
import urllib

from django import http
from django import forms
from django.conf import settings
from django.template import loader
from django.utils import simplejson
from django.core import serializers

from casam.models import Project
from casam.models import OriginalImage
from casam.models import Tag
from casam.models import PotentialMeasurement
from casam.models import PotentialMeasurementType
from casam.models import Measurement
from casam.views import handler
from casam.views import tag as tag_view


class SelectTagForm(forms.Form):
  tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)


class Home(handler.Handler):
  """Handler for the home page.
  """

  def getTags(self, tags):
    tags = [i.id for i in Tag.objects.filter(name__in=tags)]

    return tags

  def getPostForm(self):
    return SelectTagForm(self.POST)

  def get(self):
    context = self.getContext()
    tags = self.getTags(self.GET.getlist('tag'))
    projects = Project.objects.select_related()

    if tags:
      projects = projects.filter(tags__id__in=tags)

    projects = dict([(i,[]) for i in projects])

    initial = {
        'tags' : tags,
        }

    context['projects'] = projects
    context['tag_form'] = SelectTagForm(initial=initial)
    #list(tags);
    context['tags'] = [str(i) for i in tags]

    content = loader.render_to_string('main/home.html', dictionary=context)
    return http.HttpResponse(content)

  def post(self):
    tags = [i.name for i in self.cleaned_data['tags']]
    url = urllib.urlencode({'tag': tags}, doseq=True)
    return http.HttpResponseRedirect(self.path + '?' + url)

class projectsJSON(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    tags = self.GET.getlist('tags')
    projects = Project.objects.select_related()
    #print tags
    if tags:
      projects = projects.filter(tags__id__in=tags).distinct()
    data = serializers.serialize("json", projects)
    return http.HttpResponse(data, mimetype="application/javascript")
  
class deleteProjects(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    projectIDs = self.GET.getlist('projectID')
    for projectID in projectIDs:
      Project.objects.all().get(id = projectID).delete()
    return http.HttpResponse("success")
  
class deleteImages(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    imageIDs = self.GET.getlist('imageID')
    for imageID in imageIDs:
      OriginalImage.objects.all().get(id = imageID).delete()
    return http.HttpResponse("success")
  
class deleteMeasurement(handler.Handler):
  def get(self):
    potid = self.GET.getlist('potentialMeasurementID')
    imageID = self.GET.getlist('imageID')
    image = OriginalImage.objects.all().get(id = imageID[0])
    potmeas = PotentialMeasurement.objects.all().get(id = potid[0])
    Measurement.objects.all().filter(image = image, mogelijkemeting = potmeas).get().delete()
    
    return http.HttpResponse("succes")

  def getPostForm(self):
    return SelectTagForm(self.POST)
  
class deletePotentialMeasurement(handler.Handler):
  def get(self):
    potid = self.GET.getlist('potID')
    potmeas = PotentialMeasurement.objects.all().get(id = potid[0])
    Measurement.objects.all().filter(mogelijkemeting = potmeas).delete()
    PotentialMeasurement.objects.all().get(id = potid[0]).delete()
    
    return http.HttpResponse("success")
  def getPostForm(self):
    return SelectTagForm(self.POST)
    
class deletePotentialMeasurementType(handler.Handler):
  def get(self):
    typeid = self.GET.getlist('potTypeID')
    potmeas = list(PotentialMeasurement.objects.all().filter(type__id = typeid[0]))
    for potmeas in potmeas:
      Measurement.objects.all().filter(mogelijkemeting = potmeas).delete()
    PotentialMeasurement.objects.all().filter(type__id = typeid[0]).delete()
    PotentialMeasurementType.objects.all().get(id = typeid[0]).delete()
    
    return http.HttpResponse("success")
  def getPostForm(self):
    return SelectTagForm(self.POST)