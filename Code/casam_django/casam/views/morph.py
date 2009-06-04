from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from casam.logic import morph
from django import forms
from django.utils import simplejson

class MorphForm(forms.Form):
  projectID = forms.CharField(max_length=36)
  pdmData = forms.CharField()
    
class MorphCreator(handler.Handler):

  def getPostForm(self):
    return MorphForm(self.POST)

  def post(self):
    projectID = self.cleaned_data['projectID']
    pdmData = self.cleaned_data['pdmData']
    pdmDataObject = simplejson.loads(pdmData)['pdmData']
    if (len(pdmDataObject)==0):
      return http.HttpResponseServerError('Not enough landmarks selected.')
    images = []
    measurements = []
    measurecount = len((pdmDataObject[0])[1])
    for i in range(len(pdmDataObject)):
      imagemeasure = pdmDataObject[i]
      if len(imagemeasure[1]) != measurecount or len(imagemeasure[1]) == 0:
        return http.HttpResponseServerError('Incorrect number of landmarks per image selected.') 
      images.append(imagemeasure[0])
      measurements.append(imagemeasure[1])
    morphmodel, result = morph.createMorph(images,measurements)
    if result == 0:
      return http.HttpResponseServerError('Landmarks are not comparable.') 
    return http.HttpResponse('Successfully morphed.')

  
  def get(self):
    return http.HttpResponse('success')