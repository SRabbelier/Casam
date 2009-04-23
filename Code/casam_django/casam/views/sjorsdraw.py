from django.conf import settings
from django import http
from django.template import loader

def sjorsDraw(request):
  content = loader.render_to_string('draw/sjorsdrawtest.html')
  
  return http.HttpResponse(content)   