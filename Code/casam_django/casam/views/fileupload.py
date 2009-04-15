'''
Created on 15 apr 2009

@author: Jaap den Hollander
'''
from django import http
from django.template import loader
from django import forms
import time
import mimetypes
import os

class UploadFileForm(forms.Form):
  file = forms.FileField()

def fileupload(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      location = handle_uploaded_file(request.FILES['file'])
      context = {'location': location}
      content = loader.render_to_string('main/succes.html', dictionary=context)
      return http.HttpResponse(content)
  else:
    context = {'form': UploadFileForm()}
    content = loader.render_to_string('main/fileupload.html', dictionary=context)
    return http.HttpResponse(content)

def handle_uploaded_file(file):
  location = "data/%d-%s" % (time.time(), file.name)
  destination = open(location, 'wb+') #wb+ is write binary
  for chunk in file.chunks():
      destination.write(chunk)
  destination.close
  return location

def viewfile(request, name):
  mime = mimetypes.MimeTypes
  mime = mime()
  if os.path.exists('data/'+name):
    return http.HttpResponse(open('data/'+name,'rb'),mimetype=mime.guess_type('data/'+name))
  else:
    return http.HttpResponse("file doesn't exist",mimetype="text/plain")
