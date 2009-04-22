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
from casam.models import ProjectMeasurementList
from casam.models import OriginalImage
from casam.views import handler


class LandmarkForm(forms.Form):
  """TODO: dosctring
  """

  mm = forms.CharField() # TODO fix forms.UUIDField?
  x = forms.IntegerField(min_value=-5000, max_value=5000)
  y = forms.IntegerField(min_value=-5000, max_value=5000)


class LandmarkSaver(handler.Handler):
  """Handler to handle a save Landmark request.
  """

  def getGetForm(self):
    return LandmarkForm()

  def getPostForm(self):
    return LandmarkForm(self.POST)

  def get(self):
    # TODO: implement this?
    pass

  def post(self):
    mm = self.cleaned_data['mm']
    id = mm;
    mmeting = ProjectMeasurementList.objects.select_related().get(id=id);

    x = self.cleaned_data['x']
    y = self.cleaned_data['y']

    properties = dict(
        mogelijkemeting=mmeting,
        project=mmeting.project,
        x=x,
        y=y,
        )

    punt = Measurement(**properties)
    punt.save();

    context = {'x': punt.x,'y':punt.y,'mm':mmeting.name}
    content = loader.render_to_string('landmarks/landmark_save.html', dictionary=context)

    return http.HttpResponse(content)
