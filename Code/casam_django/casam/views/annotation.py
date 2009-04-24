import uuid

from django import http
from django import forms

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


class NewAnnotation(handler.Handler):
  """
  """

  def get(self):
    """
    """

    context = self.getContext()
    content = loader.render_to_string('annotation/new.html', dictionary=context)

    return http.HttpResponse(content)

  def post(self):
    """
    """

    