import sys
import os

from django import http
from django.conf import settings
from django.template import loader
from casam.models import Project
from casam.models import OriginalImage
from casam.views import handler

class Home(handler.Handler):
  """Handler for the home page.
  """

  def get(self):
    projects = dict([(i,[]) for i in Project.objects.all()])

    imgs = OriginalImage.objects.select_related().order_by('project__name')

    if imgs:
      img = imgs[0]
      projects[img.project] = img
  
    context = self.getContext();
    context['projects'] = projects

    content = loader.render_to_string('main/home.html', dictionary=context)
    return http.HttpResponse(content)




