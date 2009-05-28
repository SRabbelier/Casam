from django import http
from django import forms
from django.conf import settings
from django.core import serializers
from django.template import loader
from casam.views import handler
from casam.models import State


class ShowState(handler.Handler):
  def get(self):
    stateID = self.kwargs['uuid']
    context = self.getContext()
    selectedState = State.objects.all().get(id=stateID)
    context['stateData'] = selectedState.serializedState
    context['width'] = selectedState.width
    context['height'] = selectedState.height
    content = loader.render_to_string('state/show.html', dictionary=context)
    return http.HttpResponse(content)
  
  def authenticated(self):
    return self.profile_type == 'Onderzoeker'