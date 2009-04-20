import uuid

from django import http
from django.template import loader
from django import forms
from casam.models import OriginalImage
from casam.models import Project
from casam.models import MogelijkeMeting
from casam.models import Meting


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  description = forms.CharField(max_length=500, widget=forms.widgets.Textarea())
  mmeting1 = forms.CharField(max_length=50)
  mmeting2 = forms.CharField(max_length=50)


def home(request, id_str):
  id = uuid.UUID(id_str)
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id)
  punten = Meting.objects.select_related().filter(project__id=id);
  mmetings = MogelijkeMeting.objects.all().filter(project__id=id);
  context = {'images':img, 'id': id_str, 'mmetings':mmetings,'punten':punten}

  content = loader.render_to_string('project/home.html', dictionary=context)
  return http.HttpResponse(content)


def new(request):
  if request.method == 'POST':
    form = ProjectForm(request.POST)

    if form.is_valid():
      handle_add_project(request.POST)
      return http.HttpResponseRedirect('/')

  context = {'form': ProjectForm()}
  content = loader.render_to_string('project/new.html', dictionary=context)
  return http.HttpResponse(content)


def handle_add_project(post):
  project = Project(name=post['name'])
  project.save()
  
  mmeting1 = MogelijkeMeting(project=project, name=post['mmeting1'])
  mmeting2 = MogelijkeMeting(project=project, name=post['mmeting2'])
  mmeting1.save()
  mmeting2.save()