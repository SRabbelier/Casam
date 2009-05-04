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
from casam.models import ProjectMeasurementList
from casam.models import Measurement 
from casam.views import handler


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  description = forms.CharField(max_length=500, widget=forms.widgets.Textarea())
  mmeting1 = forms.CharField(max_length=50)
  mmeting2 = forms.CharField(max_length=50)


class Home(handler.Handler):
  """Handler for the home page.
  """

  def authenticated(self):
    read_projects = [i.id for i in self.profile.read.all()]
    return self.profile and self.kwargs['id_str'] in read_projects

  def get(self):
    context = self.getContext();
    id_str = self.kwargs['id_str']
    img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id_str)

    annotations = Annotation.objects.select_related().order_by(
        'project__name').filter(project__id=id_str)

    project = Project.objects.filter(id=id_str).get();
    punten = Measurement.objects.select_related().filter(project__id=id_str);
    mmetings = ProjectMeasurementList.objects.all().filter(project__id=id_str);

    context['annotations'] = annotations
    context['images'] = img
    context['id'] = id_str
    context['mmetings'] = mmetings
    context['punten'] = punten
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
    context = self.getContext()
    name = self.cleaned_data['name']
    mmeting1 = self.cleaned_data['mmeting1']
    mmeting2 = self.cleaned_data['mmeting2']
    description = self.cleaned_data['description']

    project_logic.handle_add_project(self.profile, name, mmeting1, mmeting2, description)

    return http.HttpResponseRedirect(self.BASE_PATH)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('project/new.html', dictionary=context)
    return http.HttpResponse(content)


def projectImagesJSON(request,id_str):
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id_str)
  data = serializers.serialize("json", img)
  return http.HttpResponse(data, mimetype="application/javascript")
