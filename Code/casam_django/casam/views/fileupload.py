import mimetypes
import os
import itertools

from PIL import Image

from django import forms
from django import http
from django.conf import settings
from django.template import loader

from casam.logic import fileupload as fileupload_logic
from casam.models import Image
from casam.models import Patient
from casam.models import Project
from casam.models import OriginalImage
from casam.views import handler


class UploadFileForm(forms.Form):
  """TODO: dosctring
  """

  is_left = forms.CharField(max_length=5,widget=forms.RadioSelect(choices=((True,"Links"),(False,"Rechts"))))

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
    user = context['USER']
    if user.is_authenticated():
      
      if not context['is_chirurg']:
        rights = itertools.chain(context['PROFILE'].read.all(), context['PROFILE'].write.all())
        
        proj_rights = dict([(i.id,[]) for i in rights])
        
        if self.kwargs['id_str'] in proj_rights:
          
          file = self.FILES['file']
          name = self.cleaned_data['name']
          is_left = self.cleaned_data['is_left']
          id_str = self.kwargs['id_str']
      
          oi = fileupload_logic.handle_uploaded_file(file, name, is_left, id_str) 
          
          context['image'] =oi 
          content = loader.render_to_string('main/succes.html', dictionary=context)
          return http.HttpResponse(content)
      else:
        return http.HttpResponseRedirect(context['BASE_PATH']+'home')
    else:
      return http.HttpResponse(context['BASE_PATH'])

  def get(self):
    context = self.getContext()
    user = context['USER']
    if user.is_authenticated():
      
      if not context['is_chirurg']:
        rights = itertools.chain(context['PROFILE'].read.all(), context['PROFILE'].write.all())
        
        proj_rights = dict([(i.id,[]) for i in rights])
        
        if self.kwargs['id_str'] in proj_rights:
          context['form'] = self.form
          content = loader.render_to_string('main/fileupload.html', dictionary=context)
          return http.HttpResponse(content)
      else:
        return http.HttpResponseRedirect(context['BASE_PATH']+'home')
    else:
      return http.HttpResponse(context['BASE_PATH'])


def viewfile(request, name):
  """TODO: Docstring
  """
  user = request.user
  if user.is_authenticated():  
    mime = mimetypes.MimeTypes
    mime = mime()
    if os.path.exists('data/'+name):
      mimetype = mime.guess_type('data/'+name)
      return http.HttpResponse(open('data/'+name,'rb'),mimetype=mimetype)
    else:
      return http.HttpResponse("file doesn't exist",mimetype="text/plain")
  else:
    return http.HttpResponseRedirect(getattr(settings, 'DATADIR'))
