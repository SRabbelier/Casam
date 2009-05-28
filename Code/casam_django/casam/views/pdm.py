from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from casam.logic import pdm
from django import forms
from django.utils import simplejson

class PDMForm(forms.Form):
  projectID = forms.CharField(max_length=36)
  pdmData = forms.CharField()
    
class PDMCreator(handler.Handler):

  def getPostForm(self):
    return PDMForm(self.POST)

  def post(self):
    projectID = self.cleaned_data['projectID']
    pdmData = self.cleaned_data['pdmData']
    pdmDataObject = simplejson.loads(pdmData)['pdmData']
    print len(pdmDataObject)
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
    pdmodel, result = pdm.createPDM(images,measurements)
    if result == 0:
      return http.HttpResponseServerError('Landmarks are not comparable.') 
    pdm.analyse(pdmodel, projectID, images)
    return http.HttpResponse('Successfully saved Point Distribution Model overlay-image to data directory.')

  
  def get(self):
    return http.HttpResponse('success')