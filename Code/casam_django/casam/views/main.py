import sys
import os
import itertools
import urllib

from django import http
from django import forms
from django.conf import settings
from django.template import loader
from django.utils import simplejson
from django.core import serializers



from casam.models import Project
from casam.models import OriginalImage
from casam.models import Tag
from casam.views import handler
from casam.views import tag as tag_view


class SelectTagForm(forms.Form):
  tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)


class Home(handler.Handler):
  """Handler for the home page.
  """

  def getTags(self, tags):
    tags = [i.id for i in Tag.objects.filter(name__in=tags)]

    return tags

  def getPostForm(self):
    return SelectTagForm(self.POST)

  def get(self):
    context = self.getContext()
    tags = self.getTags(self.GET.getlist('tag'))
    projects = Project.objects.select_related()

    if tags:
      projects = projects.filter(tags__id__in=tags)

    projects = dict([(i,[]) for i in projects])

    initial = {
        'tags' : tags,
        }

    context['projects'] = projects
    context['tag_form'] = SelectTagForm(initial=initial)
    #list(tags);
    context['tags'] = [str(i) for i in tags]

    content = loader.render_to_string('main/home.html', dictionary=context)
    return http.HttpResponse(content)

  def post(self):
    tags = [i.name for i in self.cleaned_data['tags']]
    url = urllib.urlencode({'tag': tags}, doseq=True)
    return http.HttpResponseRedirect(self.path + '?' + url)

class projectsJSON(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    tags = self.GET.getlist('tags')
    projects = Project.objects.select_related()
    #print tags
    if tags:
      projects = projects.filter(tags__id__in=tags).distinct()
    data = serializers.serialize("json", projects)
    return http.HttpResponse(data, mimetype="application/javascript")
  
class deleteProjects(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    projectIDs = self.GET.getlist('projectID')
    for projectID in projectIDs:
      Project.objects.all().get(id = projectID).delete()
    return http.HttpResponse("success")
  
class deleteImages(handler.Handler):
  def getPostForm(self):
    return SelectTagForm(self.POST)
  
  def get(self):
    #print self.cleaned_data['tags']
    imageIDs = self.GET.getlist('imageID')
    for imageID in imageIDs:
      OriginalImage.objects.all().get(id = imageID).delete()
    return http.HttpResponse("success")