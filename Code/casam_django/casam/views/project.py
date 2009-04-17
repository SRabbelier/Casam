import uuid

from django import http
from django.template import loader
from django import forms
from casam.models import OriginalImage
from casam.models import Project


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  description = forms.CharField(max_length=500, widget=forms.widgets.Textarea())


def home(request, id):
  id = uuid.UUID(id)
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id)

  context = {'images':img}

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