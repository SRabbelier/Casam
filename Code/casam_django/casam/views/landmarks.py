import uuid
import time
import mimetypes
import os

from django import http
from django.template import loader
from django import forms

from casam.django_tools import fields
from casam.models import Image
from casam.models import Patient
from casam.models import Project
from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import OriginalImage
from casam.views import handler
from django.conf import settings

import Image

class LandmarkForm(forms.Form):
  """TODO: dosctring
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
    # TODO: implement this?
    return http.HttpResponse("GTFO")

  def post(self):
    context = self.getContext()
    mm = self.cleaned_data['mm']
    id = mm;
    img = OriginalImage.objects.filter(id=self.cleaned_data['imgid']).get()
    mmeting = PotentialMeasurement.objects.select_related().get(id=id);
      
    #lets check if there is already one measurement for this image of this type
    try:
      meting = Measurement.objects.filter(mogelijkemeting=mmeting, image=img).get()
    except Measurement.DoesNotExist:
      meting = None

    location = "./" + settings.DATADIR + "%s" % (img.path)
    im = Image.open(location)
    piecex = float(self.cleaned_data['imagewidth']) / im.size[0]
    piecey = float(self.cleaned_data['imageheight']) / im.size[1]
    
    

    properties = dict(
        mogelijkemeting=mmeting,
        image=img,
        x=int(float(self.cleaned_data['x'])/piecex),
        y=int(float(self.cleaned_data['y'])/piecey),
        imagewidth=im.size[0],
        imageheight=im.size[1]
        )
    
    punt = Measurement(**properties)
    if meting:
      punt.id = meting.id;
    punt.save();

#    context['x'] = punt.x
#    context['y'] = punt.y
#    context['mm'] = mmeting.name
#    context['name'] = img.name
#    context['id'] = img.id
#    context['piecex'] = piecex
#    context['piecey'] = piecey
#    content = loader.render_to_string('landmarks/landmark_save.html', dictionary=context)

    return http.HttpResponse()
