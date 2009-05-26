import uuid
import urllib

from django import http
from django import forms
from django.template import loader

from casam.logic import annotation as annotation_logic
from casam.logic import fileupload as fileupload_logic
from casam.views import handler
from casam.models import Annotation

from django.conf import settings



CHOICES = [
    ('url', 'Use an existing url'),
    ('file', 'Upload a new file'),
    ]


class SelectTypeForm(forms.Form):
  type = forms.ChoiceField(CHOICES)


class FileAnnotationForm(forms.Form):
  name = forms.CharField(max_length=50)
  file = forms.FileField()


class UrlAnnotationForm(forms.Form):
  name = forms.CharField(max_length=50)
  url = forms.URLField()


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
    if self.GET.get('type') == 'url':
      return UrlAnnotationForm()

    if self.GET.get('type') == 'file':
      return FileAnnotationForm()

    return SelectTypeForm()

  def getPostForm(self):
    if self.GET.get('type') == 'url':
      return UrlAnnotationForm(self.POST)

    if self.GET.get('type') == 'file':
      return FileAnnotationForm(self.POST, self.FILES)

    return SelectTypeForm(self.POST)

  def get(self):
    context = self.getContext()

    if self.GET.get('type') not in ['file', 'url']:
      context['submit_value'] = 'choose'

    content = loader.render_to_string('annotation/new.html', dictionary=context)

    return http.HttpResponse(content)

  def post(self):
    annotation_type = self.GET.get('type')

    if annotation_type not in ['file', 'url']:
      annotation_type = self.cleaned_data['type']
      url = self.path + '?' + urllib.urlencode({'type': annotation_type})
      return http.HttpResponseRedirect(url)

    project_id = self.kwargs['uuid']
    name = self.cleaned_data['name']

    if annotation_type == 'url':
      url = self.cleaned_data['url']

    if annotation_type == 'file':
      file = self.FILES['file']
      location = fileupload_logic.handle_uploaded_file(file, name)
      url = settings.BASE_PATH + location[0]

    # TODO : rewrite this to use UUID instead of original filename
    annotation_logic.handle_add_annotation(name, url, project_id)

    return http.HttpResponseRedirect(settings.BASE_PATH)
