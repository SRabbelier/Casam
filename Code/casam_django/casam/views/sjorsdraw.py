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

class BrushStrokeForm(forms.Form):
  """TODO: dosctring
  """
  fileName = forms.CharField(max_length=50)
  brushStroke = JSONFormField()
  


class sjorsDraw(handler.Handler):
  def get(self):
    content = loader.render_to_string('draw/sjorsdrawtest.html')
    return http.HttpResponse(content)
  
class AddBrushStroke(handler.Handler):
  
  def getPostForm(self):
    return BrushStrokeForm(self.POST)
  
  def get(self):
    return http.HttpResponse("")
  
  def post(self):
    brushStroke = self.cleaned_data['brushStroke']
    fileName = self.cleaned_data['fileName']
    #print self.cleaned_data['brushStroke']
    #im = Image.open(fileName,"RGBA")
    if os.path.exists(fileName):
      im = Image.open(fileName)
      im = im.convert("RGBA")
    else:
      im = Image.new("RGBA",(900,300))
    draw = ImageDraw.Draw(im)

    positions = brushStroke['positions']
    #print brushStroke
    #DRAWING CODE HERE
    
    previousPosition = 0
    positionList = []
    for position in positions:
      positionList.append(position[0])
      positionList.append(position[1])
      
    draw.line(positionList,fill=(255,0,0,100),width=3)
    #print positionList
    
    
    #print brushStroke.positions;
    
    del draw
    im.save(fileName,transparency=0)
    
    
    #wrapper = FileWrapper(file(fileName))
    #response = http.HttpResponse(wrapper, content_type='image/gif')
    #response['Content-Length'] = os.path.getsize(fileName)
    response = http.HttpResponse('{\"message\":\"reload\"}')
    return response