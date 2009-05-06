from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from django import forms
from casam.django_tools.fields import JSONFormField
import Image, ImageDraw
from django.core.servers.basehttp import FileWrapper
import os
from django.utils import simplejson as json
from casam.logic import bitmap_dump as bitmap_dump_logic

# New code that can save each json bitmap_stream
class Save(handler.Handler):
  def post(self):
    bitmap_dump_logic.handle_bitmap_stream(self)

    response = http.HttpResponse('{\"message\":\"reload\"}')
    return response



# Old code that returns Post-form
class BrushStrokeForm(forms.Form):
  """TODO: dosctring
  """
  fileName = forms.CharField(max_length=50)
  brushStroke = JSONFormField()
  

# Old code that returns SjorsDraw page
class sjorsDraw(handler.Handler):
  def get(self):
    content = loader.render_to_string('draw/sjorsdrawtest.html')
    return http.HttpResponse(content)
  
# Old code that saves a post SjorsDraw
class AddBrushStroke(handler.Handler):
  
  def getPostForm(self):
    return BrushStrokeForm(self.POST)
  
  def get(self):
    return http.HttpResponse("")
  
  def post(self):
    bitmap_dump_logic.handle_bitmap_stream(self)

    response = http.HttpResponse('{\"message\":\"reload\"}')
    return response