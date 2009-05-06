'''
Created on Mei 6, 2009

@author: bbijl
'''
from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler

class Main(handler.Handler):

  def get(self):
  
    context = self.getContext();
    content = loader.render_to_string('draw/paint.html', dictionary=context)
  
    return http.HttpResponse(content)       