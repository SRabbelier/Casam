import uuid

from django import http
from django import forms
from django.conf import settings
from django.core import serializers
from django.template import loader

from casam.logic import project as project_logic
from casam.models import OriginalImage
from casam.models import Project
from casam.models import MogelijkeMeting
from casam.models import Meting 
from casam.views import handler


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  description = forms.CharField(max_length=500, widget=forms.widgets.Textarea())
  mmeting1 = forms.CharField(max_length=50)
  mmeting2 = forms.CharField(max_length=50)


class Home(handler.Handler):
  """Handler for the home page.
  """

  def get(self):
    DATADIR = '../' + settings.DATADIR

    id_str = self.kwargs['id_str']
    id = uuid.UUID(id_str)

    img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id)

    punten = Meting.objects.select_related().filter(project__id=id);
    mmetings = MogelijkeMeting.objects.all().filter(project__id=id);

    context = {'images':img, 'id': id_str, 'mmetings':mmetings,'punten':punten, 'DATADIR':DATADIR}
  
    content = loader.render_to_string('project/home.html', dictionary=context)

    return http.HttpResponse(content)


class NewProject(handler.Handler):
  """Handler for the creation of a new project.
  """

  def getGetForm(self):
    return ProjectForm()

  def getPostForm(self):
    return ProjectForm(self.POST)

  def post(self):
    name = self.cleaned_data['name']
    mmeting1 = self.cleaned_data['mmeting1']
    mmeting2 = self.cleaned_data['mmeting2']

    project_logic.handle_add_project(name, mmeting1, mmeting2)

    return http.HttpResponseRedirect('/')

  def get(self):
    context = {'form': self.form}
    content = loader.render_to_string('project/new.html', dictionary=context)
    return http.HttpResponse(content)


def projectImagesJSON(request,id_str):
  id = uuid.UUID(id_str)
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id)
  data = serializers.serialize("json", img)
  return http.HttpResponse(data, mimetype="application/javascript")
