from django import http
from django.template import loader
from ..models import OriginalImage
from ..models import Project

def home(request):
  img = OriginalImage.objects.select_related().order_by('project__name')
  
  #img = OriginalImage.objects.select_related()
  #print img
  context = {'images':img}
  
  content = loader.render_to_string('main/home.html', dictionary=context)
  return http.HttpResponse(content)
