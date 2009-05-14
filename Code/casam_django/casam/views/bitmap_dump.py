from django import http
from django import forms
from django.conf import settings
from django.template import loader
from casam.views import handler
from casam.models import OriginalImage
from casam.logic.bitmap_dump import handle_bitmap_stream

class BitmapForm(forms.Form):
  dump = forms.CharField(max_length=36000000)
  image_id = forms.CharField(max_length=36)
  
  
class Save(handler.Handler):
  def getPostForm(self):
    return BitmapForm(self.POST)
  
  def getGetForm(self):
    return BitmapForm()
  
  def post(self):
    self.getContext()
    original_image = OriginalImage.objects.filter(id=self.cleaned_data['image_id']).get()
    filename = handle_bitmap_stream(self.cleaned_data['dump'],self.cleaned_data['image_id'],original_image)
    return http.HttpResponse("filename="+filename)