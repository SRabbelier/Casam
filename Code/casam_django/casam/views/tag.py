from django import http
from django import forms
from django.template import loader

from casam.models import Project
from casam.models import Tag
from casam.logic import tag as tag_logic
from casam.views import handler


class SelectTagForm(forms.Form):
  tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)


class TagForm(forms.Form):
  name = forms.CharField(max_length=50)


class NewTag(handler.Handler):
  """Handler for the creation of a new tag.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def getGetForm(self):
    return TagForm()

  def getPostForm(self):
    return TagForm(self.POST)

  def post(self):
    name = self.cleaned_data['name']

    id_str = self.kwargs['id_str']
    project = Project.objects.filter(id=id_str).get()
    tag_logic.handle_add_tag(project, name)

    return http.HttpResponseRedirect(self.BASE_PATH + 'tag/select/' + id_str)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('tag/new.html', dictionary=context)
    return http.HttpResponse(content)


class SelectTag(handler.Handler):
  """Handler to select an existing tag.
  """

  def authenticated(self):
    proj = self.kwargs['id_str']
    return self.profile and proj in [i.id for i in self.profile.read.all()]

  def getGetForm(self):
    proj_id = self.kwargs['id_str']
    project = Project.objects.filter(id=proj_id).get()
    initial = {
        'tags': [i.id for i in project.tags.all()],
        }
    return SelectTagForm(initial=initial)

  def getPostForm(self):
    return SelectTagForm(self.POST)

  def post(self):
    tags = self.cleaned_data.get('tags', [])

    id_str = self.kwargs['id_str']
    project = Project.objects.filter(id=id_str).get()
    tag_logic.handle_select_tags(project, tags)

    return http.HttpResponseRedirect(self.BASE_PATH + 'project/show/' + id_str)

  def get(self):
    context = self.getContext()
    context['id'] = self.kwargs['id_str']
    content = loader.render_to_string('tag/select.html', dictionary=context)
    return http.HttpResponse(content)
