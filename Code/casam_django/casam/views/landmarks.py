import uuid
import time
import mimetypes
import os

from django import http
from django.template import loader
from django import forms
from django.core import serializers

from casam.django_tools import fields
from casam.models import Image
from casam.models import Project
from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import OriginalImage
from casam.views import handler
from django.conf import settings

import Image

class LandmarkForm(forms.Form):
  """Form to load in the website to create a measurement
  """

  mm = forms.CharField() # TODO fix forms.UUIDField?
  x = forms.IntegerField(min_value=-5000, max_value=5000)
  y = forms.IntegerField(min_value=-5000, max_value=5000)
  imgid = forms.CharField(widget = forms.widgets.HiddenInput())
  imagewidth = forms.CharField(widget = forms.widgets.HiddenInput())
  imageheight = forms.CharField(widget = forms.widgets.HiddenInput())


class LandmarkSaver(handler.Handler):
  """Handler to handle a save Landmark request.
  """

  def getGetForm(self):
    return LandmarkForm()

  def getPostForm(self):
    return LandmarkForm(self.POST)
  
  def get(self):
    return http.HttpResponse('Not implemented')

  def post(self):
    context = self.getContext()
    mm = self.cleaned_data['mm']
    id = mm;
    img = OriginalImage.objects.filter(id=self.cleaned_data['imgid']).get()
    mmeting = PotentialMeasurement.objects.select_related().get(id=id);
    
    #the saved measurement cannot be of the 'bitmap' type
    if (mmeting.soort == 'B'):
      return http.HttpResponseServerError()
      
    #lets check if there is already one measurement for this image of this type
    try:
      meting = Measurement.objects.filter(mogelijkemeting=mmeting, image=img).get()
    except Measurement.DoesNotExist:
      meting = None

    #get the image from file, to look at it's size
    location = os.path.join(settings.DATADIR, img.id + '.jpg')
    im = Image.open(location)
    piecex = float(self.cleaned_data['imagewidth']) / im.size[0]
    piecey = float(self.cleaned_data['imageheight']) / im.size[1]
    
    properties = dict(
      mogelijkemeting=mmeting,
      image=img,
      x=int(round(float(self.cleaned_data['x'])/piecex)),
      y=int(round(float(self.cleaned_data['y'])/piecey)),
      imagewidth=im.size[0],
      imageheight=im.size[1],
      project=img.project
    )
    
    punt = Measurement(**properties)
    #overwrite the potentially existing measurement
    if meting:
      punt.id = meting.id;
    punt.save();

    data = serializers.serialize("json", [punt])
    return http.HttpResponse(data, mimetype="application/javascript")
