import uuid

from django import http
from django import forms
from django.template import loader

from casam.logic import annotation as annotation_logic
from casam.logic import fileupload as fileupload_logic
from casam.views import handler
from casam.models import Annotation


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=50)
  url = forms.URLField()
  file = forms.FileField()


class ViewAnnotation(handler.Handler):
  """Handler for the home page.
  """

  def get(self):
    id = self.kwargs['uuid']

    try:
      annotation = Annotation.objects.select_related().get(id=id)
    except Annotation.DoesNotExist, exception:
      return http.HttpResponse('No such annotation')

    context = self.getContext()

    context['annotation'] = annotation

    content = loader.render_to_string('annotation/show.html', dictionary=context)
    return http.HttpResponse(content)


class ListAnnotations(handler.Handler):
  """List annotations using ViewAnnotation.
  """

  def get(self):
    project_id = self.kwargs['uuid']

    annotations = Annotation.objects.select_related().order_by(
        'project__name').filter(project__id=project_id)

    context = self.getContext()
    context['annotations'] = annotations

    content = loader.render_to_string('annotation/list.html', dictionary=context)
    return http.HttpResponse(content)


class NewAnnotation(handler.Handler):
  """Create a new Annotation.
  """

  def getGetForm(self):
    return ProjectForm()

  def getPostForm(self):
    return ProjectForm(self.POST, self.FILES)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('annotation/new.html', dictionary=context)

    return http.HttpResponse(content)

  def post(self):
    project_id = self.kwargs['uuid']
    name = self.cleaned_data['name']
    url = self.cleaned_data['url']
    file = self.FILES['file']
    annotation_logic.handle_add_annotation(name, url, project_id)
    oi = fileupload_logic.handle_uploaded_file(file, name)
    context = self.getContext()

    return http.HttpResponseRedirect(context['BASE_PATH']+'home') 
