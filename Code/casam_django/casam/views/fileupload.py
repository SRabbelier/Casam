'''
Created on 15 apr 2009

@author: Jaap den Hollander
'''
from django import http
from django.template import loader
from django import forms
from casam.models import Image
from casam.models import Patient
from casam.models import OriginalImage

import time
import mimetypes
import os

class UploadFileForm(forms.Form):
  name = forms.CharField(max_length=50)
  file = forms.FileField()

def fileupload(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      oi = handle_uploaded_file(request.FILES['file'],request.POST['name'])
      context = {'image': oi}
      content = loader.render_to_string('main/succes.html', dictionary=context)
      return http.HttpResponse(content)
  else:
    context = {'form': UploadFileForm()}
    content = loader.render_to_string('main/fileupload.html', dictionary=context)
    return http.HttpResponse(content)

def handle_uploaded_file(file,name):
  location = "data/%d-%s" % (time.time(), file.name)
  destination = open(location, 'wb+') #wb+ is write binary
  for chunk in file.chunks():
      destination.write(chunk)
  destination.close
  #Image.objects.all()
  Patient.objects.all()
  OriginalImage.objects.all()
  pat = Patient(corpse_id=234,sex=True)
  pat.save()
  #i = Image()
  #i.save()
  OriginalImage()
  oi = OriginalImage(patient=pat,name=name,path=location,is_left=False)
  oi.save()
  return oi

def viewfile(request, name):
  mime = mimetypes.MimeTypes
  mime = mime()
  if os.path.exists('data/'+name):
    return http.HttpResponse(open('data/'+name,'rb'),mimetype=mime.guess_type('data/'+name))
  else:
    return http.HttpResponse("file doesn't exist",mimetype="text/plain")
