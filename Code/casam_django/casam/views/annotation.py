import uuid

from django import http
from django import forms
from django.template import loader

from casam.logic import annotation as annotation_logic
from casam.views import handler
from casam.models import Annotation


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  url = forms.URLField()


class ViewAnnotation(handler.Handler):
  """Handler for the home page.
  """

  def get(self):
    """
    """

    id = self.kwargs['uuid']

    try:
      annotation = Annotation.objects.select_related().get(id=id)
    except Annotation.DoesNotExist, exception:
      return http.HttpResponse('No such annotation')

    context = self.getContext()

    context['annotation'] = annotation

    content = loader.render_to_string('annotation/show.html', dictionary=context)
    return http.HttpResponse(content)



class NewAnnotation(handler.Handler):
  """
  """

  def getGetForm(self):
    return ProjectForm()

  def getPostForm(self):
    return ProjectForm(self.POST)

  def get(self):
    """
    """

    context = self.getContext()
    content = loader.render_to_string('annotation/new.html', dictionary=context)

    return http.HttpResponse(content)

  def post(self):
    """
    """

    name = self.cleaned_data['name']
    url = self.cleaned_data['url']
    annotation_logic.handle_add_annotation(name, url)
    context = self.getContext()

    return http.HttpResponseRedirect(context['BASE_PATH']+'home') 
