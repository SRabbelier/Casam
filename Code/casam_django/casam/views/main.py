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
    context = self.getContext();
    user = context['USER']
    if user.is_authenticated():    
      projects = dict([(i,[]) for i in Project.objects.all()])

      imgs = OriginalImage.objects.select_related().order_by('project__name')

      if imgs:
        img = imgs[0]
        projects[img.project] = img
  
    
      context['projects'] = projects

      content = loader.render_to_string('main/home.html', dictionary=context)
      return http.HttpResponse(content)
    else:
      return http.HttpResponseRedirect(context['BASE_PATH'])
