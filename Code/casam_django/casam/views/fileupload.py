import mimetypes
import os

import Image

from django import forms
from django import http
from django.conf import settings
from django.template import loader

from casam.logic import fileupload as fileupload_logic
from casam.models import Image
from casam.models import Patient
from casam.models import Project
from casam.models import OriginalImage


class UploadFileForm(forms.Form):
  """TODO: dosctring
  """

  is_left = forms.CharField(max_length=5,widget=forms.RadioSelect(choices=((True,"Links"),(False,"Rechts"))))

  name = forms.CharField(max_length=50)
  file = forms.FileField()


def fileupload(request, id_str):
  """TODO: Docstring
  """

  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
      oi = fileupload_logic.handle_uploaded_file(request.FILES['file'],
                                                 request.POST, id_str)

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


def viewfile(request, name):
  """TODO: Docstring
  """

  mime = mimetypes.MimeTypes
  mime = mime()
  if os.path.exists('data/'+name):
    mimetype, _ = mime.guess_type('data/'+name)
    return http.HttpResponse(open('data/'+name,'rb'),mimetype=mimetype)
  else:
    return http.HttpResponse("file doesn't exist",mimetype="text/plain")
