from django import http
from django.template import loader

def home(request):
  context = {}
  content = loader.render_to_string('main/home.html', dictionary=context)
  return http.HttpResponse(content)
