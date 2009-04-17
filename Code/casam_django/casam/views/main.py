import sys
import os

HERE = os.path.abspath(__file__)
HERE = os.path.join(os.path.dirname(HERE), '..', '..')
HERE = os.path.normpath(HERE)

CASAM = [os.path.join(HERE, 'casam')]
sys.path = CASAM + sys.path

from django import http
from django.template import loader
from casam.models import Project
from casam.models import OriginalImage

def home(request):
  projects = dict([(i,[]) for i in Project.objects.all()])

  imgs = OriginalImage.objects.select_related().order_by('project__name')

  for img in imgs:
    projects[img.project] += [img]

  context = {'projects': projects}

  content = loader.render_to_string('main/home.html', dictionary=context)
  return http.HttpResponse(content)
