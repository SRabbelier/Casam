'''
Created on Apr 23, 2009

@author: nnsmit
'''
from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler

class Main(handler.Handler):

  def get(self):
  
    context = self.getContext();
    content = loader.render_to_string('draw/draw.html', dictionary=context)
  
    return http.HttpResponse(content)       