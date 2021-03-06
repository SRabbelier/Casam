import mimetypes
import os
import itertools

from PIL import Image

from django import forms
from django import http
from django.conf import settings
from django.template import loader
from django.core import serializers

from casam.logic import image as image_logic
from casam.logic import fileupload as fileupload_logic
from casam.models import Image
from casam.models import Project
from casam.models import OriginalImage
from casam.views import handler


class UploadFileForm(forms.Form):
  """TODO: dosctring
  """

  name = forms.CharField(max_length=50)
  file = forms.FileField()


class FileUpload(handler.Handler):
  """Handler to handle a File Upload request.
  """

  def getPostForm(self):
    return UploadFileForm(self.POST, self.FILES)

  def getGetForm(self):
    return UploadFileForm()

  def post(self):
    context = self.getContext()

    file = self.FILES['file']
    name = self.cleaned_data['name']
    id_str = self.kwargs['id_str']

    oi = image_logic.handle_uploaded_image(file, name, id_str)
    context['id'] = id_str
    context['oi'] = serializers.serialize("json",[oi])
    content = loader.render_to_string('main/succes.html', dictionary=context)
    return http.HttpResponse(content)

  def get(self):
    context = self.getContext()
    id_str = self.kwargs['id_str']
    context['id'] = id_str

    content = loader.render_to_string('main/fileupload.html', dictionary=context)
    return http.HttpResponse(content)

class ViewFile(handler.Handler):
  """TODO: Docstring
  """

  def get(self):
    user = self.user
    name = self.kwargs['img_name']

    mimetype, picture = fileupload_logic.load_file(name)

    if mimetype and picture:
      return http.HttpResponse(picture,mimetype=mimetype)

    content = "file '%s' doesn't exist" % name
    return http.HttpResponse(content,mimetype="text/plain")
