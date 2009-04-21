from django import http
from django.template import loader
from django import forms
from ..models import Image
from ..models import Patient
from ..models import Project
from ..models import OriginalImage
from django.conf import settings

import uuid
import time
import mimetypes
import os
import Image

class UploadFileForm(forms.Form):
  is_left = forms.CharField(max_length=5,widget=forms.RadioSelect(choices=((True,"Links"),(False,"Rechts"))))

  name = forms.CharField(max_length=50)
  file = forms.FileField()


def fileupload(request, id_str):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
      oi = handle_uploaded_file(request.FILES['file'],request.POST, id_str)
      DATADIR = "../"+getattr(settings, 'DATADIR')
      context = {'image': oi, 'DATADIR':DATADIR}
      content = loader.render_to_string('main/succes.html', dictionary=context)
      return http.HttpResponse(content)
    else:
      print form.errors
  else:
    pass

  context = {'form': UploadFileForm()}
  content = loader.render_to_string('main/fileupload.html', dictionary=context)
  return http.HttpResponse(content)

def handle_uploaded_file(file,post, id_str):
  DATADIR = getattr(settings, "DATADIR")
  timestamp = time.time()
  fileNameOnly = "%d-%s" % (timestamp, file.name)
  location = DATADIR+"%d-%s" % (timestamp, file.name)
  destination = open(location, 'wb+') #wb+ is write binary
  for chunk in file.chunks():
      destination.write(chunk)
  destination.close()
  
  #open the file and create a thumbnail out of it
  fullImage = Image.open(location)
  fullImageWidth = fullImage.size[0]
  fullImageHeight = fullImage.size[1]
  squareSize = min(fullImageWidth, fullImageHeight)
  box = ((fullImageWidth-squareSize)/2,(fullImageHeight-squareSize)/2,(fullImageWidth-squareSize)/2+squareSize,(fullImageHeight-squareSize)/2+squareSize)
  fullImage = fullImage.crop(box)
  
  
  sizes = 50,100,200,300
  for singleSize in sizes:
      thumbnailLocation = DATADIR+"thumbnail/%d/%d-%s" % (singleSize,timestamp, file.name)
      thumbnail=fullImage.copy()
      thumbnail.thumbnail((singleSize,singleSize),Image.ANTIALIAS)
      thumbnail.save(thumbnailLocation)
  
  #temporarly create a patient object
  #because we need this info
  Patient.objects.all()
  pat = Patient(corpse_id=234,sex=True)
  pat.save()
  #safe the uploaded image
  OriginalImage.objects.all()
  
  proj = Project.objects.get(id=uuid.UUID(id_str))
  oi = OriginalImage(patient=pat,name=post['name'],path=fileNameOnly,is_left=post['is_left'],project=proj)
  oi.save()
  return oi

def viewfile(request, name):
  mime = mimetypes.MimeTypes
  mime = mime()
  if os.path.exists('data/'+name):
    mimetype, _ = mime.guess_type('data/'+name)
    return http.HttpResponse(open('data/'+name,'rb'),mimetype=mimetype)
  else:
    return http.HttpResponse("file doesn't exist",mimetype="text/plain")
