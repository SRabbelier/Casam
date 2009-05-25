from django import forms
from django import http
from django.template import loader
from django.core import serializers

from casam.models import Project
from casam.models import PotentialMeasurement
from casam.models import PotentialMeasurementType as Type
from casam.logic import potential_measurement as potential_measurement_logic
from casam.views import handler


class PotentialMeasurementForm(forms.Form):
  name = forms.CharField(max_length=50)
  type = forms.ModelChoiceField(Type.objects.all(), empty_label=None)
  
class PotentialMeasurementTypeForm(forms.Form):
  name = forms.CharField(max_length=40)


class NewPotentialMeasurement(handler.Handler):
  """Handler for the creation of a new potential measurement.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def getGetForm(self):
    return PotentialMeasurementForm()

  def getPostForm(self):
    return PotentialMeasurementForm(self.POST)

  def post(self):
    name = self.cleaned_data['name']
    type = self.cleaned_data['type']

    id_str = self.kwargs['id_str']
    project = Project.objects.filter(id=id_str).get()
    potmeas = potential_measurement_logic.handle_add_potential_measurement(project, type, name)
    
    context = self.getContext()
    if potmeas == None:
      context['potmeas'] = ''
    else:
      context['potmeas'] = serializers.serialize("json",[potmeas]+[potmeas.type])
    content = loader.render_to_string('potential_measurement/success.html', dictionary=context)
    return http.HttpResponse(content)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('potential_measurement/new.html', dictionary=context)
    return http.HttpResponse(content)

class NewPotentialMeasurementType(handler.Handler):
  """Handler for the creation of a new potential measurement type.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def getGetForm(self):
    return PotentialMeasurementTypeForm()

  def getPostForm(self):
    return PotentialMeasurementTypeForm(self.POST)
  
  def post(self):
    name = self.cleaned_data['name']
    
    id_str = self.kwargs['id_str']
    project = Project.objects.filter(id=id_str).get()
    
    potmeastype = potential_measurement_logic.handle_add_potential_measurement_type(project, name)
    
    context = self.getContext()
    if potmeastype == None:
      context['potmeastype'] = ''
    else:
      context['potmeastype'] = serializers.serialize("json",[potmeastype])    
    content = loader.render_to_string('potential_measurement/success.html', dictionary=context)
    return http.HttpResponse(content)
    
  def get(self):
    context = self.getContext()
    content = loader.render_to_string('potential_measurement/new_type.html', dictionary=context)
    return http.HttpResponse(content)    