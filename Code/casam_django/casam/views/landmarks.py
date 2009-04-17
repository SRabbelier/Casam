'''
Created on 17 apr 2009

@author: Jaap den Hollander
'''

from django import http
from django.template import loader
from django import forms
from ..models import Image
from ..models import Patient
from ..models import Project
from ..models import OriginalImage

import uuid
import time
import mimetypes
import os

def save(request):
  context = {'x': request.POST['x'],'y':request.POST['y']}
  content = loader.render_to_string('landmarks/landmark_save.html', dictionary=context)
  return http.HttpResponse(content)