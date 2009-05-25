import uuid
import itertools

from django import http
from django import forms
from django.conf import settings
from django.core import serializers
from django.template import loader

from casam.logic import project as project_logic
from casam.models import Annotation
from casam.models import OriginalImage
from casam.models import Project
from casam.models import PotentialMeasurement
from casam.models import Measurement
from casam.models import Tag
from casam.models import Bitmap
from casam.views import handler


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  description = forms.CharField(max_length=500, widget=forms.widgets.Textarea())


class Home(handler.Handler):
  """Handler for the home page.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def get(self):
    context = self.getContext()
    id_str = self.kwargs['id_str']

    annotations = Annotation.objects.select_related().order_by(
        'project__name').filter(project__id=id_str)

    project = Project.objects.filter(id=id_str).get()
    #punten = Measurement.objects.select_related().filter(project__id=id_str)

    context['annotations'] = annotations
    context['id'] = id_str
    #context['punten'] = punten
    context['project'] = project

    content = loader.render_to_string('project/home.html', dictionary=context)

    return http.HttpResponse(content)


class NewProject(handler.Handler):
  """Handler for the creation of a new project.
  """

  def authenticated(self):
    return self.profile_type == 'Onderzoeker'

  def getGetForm(self):
    return ProjectForm()

  def getPostForm(self):
    return ProjectForm(self.POST)

  def post(self):
    name = self.cleaned_data['name']
    description = self.cleaned_data['description']

    project_logic.handle_add_project(self.profile, name, description)

    return http.HttpResponseRedirect(self.BASE_PATH)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('project/new.html', dictionary=context)
    return http.HttpResponse(content)


class ImageManager(handler.Handler):
  """Handler for the home page.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def get(self):
    context = self.getContext()
    id_str = self.kwargs['id_str']
    img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id_str)

    project = Project.objects.filter(id=id_str).get()
    #punten = Measurement.objects.select_related().filter(project__id=id_str)

    context['images'] = img
    context['id'] = id_str

    content = loader.render_to_string('project/imageManager.html', dictionary=context)

    return http.HttpResponse(content)



def projectImagesJSON(request,id_str):
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id_str)
  data = serializers.serialize("json", img)
  return http.HttpResponse(data, mimetype="application/javascript")

def projectTagsJSON(request,id_str):
  tags = Tag.objects.select_related().filter(projects__id=id_str)
  data = serializers.serialize("json", tags)
  return http.HttpResponse(data, mimetype="application/javascript")

def projectPotentialMeasurementsJSON(request,id_str):
  mmetings = list(PotentialMeasurement.objects.select_related().filter(project__id=id_str))
  mm = list()
  for m in mmetings:
    mm = mm + [m] + [m.type]
  data = serializers.serialize("json", mm)
  return http.HttpResponse(data, mimetype="application/javascript")

def projectImageCurrentMeasurementsJSON(request, id_str):
  measurements = list(Measurement.objects.select_related().filter(image__id=id_str))
  mm = list()
  for m in measurements:
    mm = mm + [m.mogelijkemeting] + [m]
  data = serializers.serialize("json", mm)
  return http.HttpResponse(data, mimetype="application/javascript")

def projectImageBitmapsJSON(request, id_str):
  bitmaps = Bitmap.objects.filter(image__id=id_str)
  data = serializers.serialize("json", bitmaps)
  return http.HttpResponse(data, mimetype="application/javascript")