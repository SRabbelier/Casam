'''
Created on 17 apr 2009

@author: Jaap den Hollander
'''
import uuid

from django import http
from django.template import loader
from django import forms
from ..models import Image
from ..models import Patient
from ..models import Project
from ..models import Meting
from ..models import MogelijkeMeting
from ..models import OriginalImage

import uuid
import time
import mimetypes
import os

def save(request):
  id = uuid.UUID(request.POST['mm']);
  mmeting = MogelijkeMeting.objects.select_related().get(id=id);
  punt = Meting(mogelijkemeting=mmeting,project=mmeting.project, x=request.POST['x'],y=request.POST['y'])
  punt.save();
  
  context = {'x': punt.x,'y':punt.y,'mm':mmeting.name}
  content = loader.render_to_string('landmarks/landmark_save.html', dictionary=context)
  return http.HttpResponse(content)