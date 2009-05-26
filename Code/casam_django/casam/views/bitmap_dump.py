from django import http
from django import forms
from django.conf import settings
from django.template import loader
from casam.views import handler
from casam.models import OriginalImage
from casam.logic.bitmap_dump import handle_bitmap_stream

class BitmapForm(forms.Form):
  image_id = forms.CharField(max_length=36)
  previous_id = forms.CharField(max_length=36)
  dump = forms.CharField(max_length=36000000)
  r = forms.CharField(max_length=3)
  g = forms.CharField(max_length=3)
  b = forms.CharField(max_length=3)
  
  
class Save(handler.Handler):
  def getPostForm(self):
    return BitmapForm(self.POST)
  
  def getGetForm(self):
    return BitmapForm()
  
  def post(self):
    self.getContext()
    r = int(self.cleaned_data['r'])
    g = int(self.cleaned_data['g'])
    b = int(self.cleaned_data['b'])
    original_image = OriginalImage.objects.filter(id=self.cleaned_data['image_id']).get()
    previous_id = self.cleaned_data['previous_id']
    bitmap_id = handle_bitmap_stream(self.cleaned_data['dump'],self.cleaned_data['image_id'],original_image,previous_id,r,g,b)
    return http.HttpResponse("saved_id="+bitmap_id)