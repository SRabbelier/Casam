from django import http
from django.template import loader
from casam.models import OriginalImage
from casam.models import Project

def home(request):
  context = {'name': 'ben','images':OriginalImage.objects.all(), 'projects': Project.objects.all()}
  content = loader.render_to_string('main/home.html', dictionary=context)
  return http.HttpResponse(content)
