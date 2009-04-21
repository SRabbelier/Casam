import uuid

from django import http
from django import forms
from django.conf import settings
from django.core import serializers
from django.template import loader

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
  mm1 = MogelijkeMeting(name=post['mmeting1'], project=project)
  mm1.save()
  mm2 = MogelijkeMeting(name=post['mmeting2'], project=project)
  mm2.save()
  
def projectImagesJSON(request,id_str):
  id = uuid.UUID(id_str)
  img = OriginalImage.objects.select_related().order_by('project__name').filter(project__id=id)
  data = serializers.serialize("json", img)
  return http.HttpResponse(data, mimetype="application/javascript")
