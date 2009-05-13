from django import http
from django import forms
from django.conf import settings
from django.template import loader
from casam.views import handler
from casam.logic.bitmap_dump import handle_bitmap_stream

class BitmapForm(forms.Form):
  dump = forms.CharField(max_length=36000000)
  
  
class Save(handler.Handler):
  def getPostForm(self):
    return BitmapForm(self.POST)
  
  def getGetForm(self):
    return BitmapForm()
  
  def post(self):
    self.getContext()
    handle_bitmap_stream(self.cleaned_data['dump'])
    return http.HttpResponse("dankje")