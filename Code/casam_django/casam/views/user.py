import uuid

from django import http
from django.template import loader
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

from casam.logic import user as user_logic
from casam.logic import user_profile as user_profile_logic
from casam.models import OriginalImage
from casam.models import Project
from casam.models import ProjectMeasurementList
from casam.models import Measurement
from casam.views import handler


class UserForm(forms.Form):
  """TODO: Docstring """

  choices = []
  projects = Project.objects.all()

  for pr in projects:
    choices.append((pr.id,pr.name))

  login = forms.CharField(max_length=30)
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.ModelChoiceField(Group.objects.all())
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  read = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)
  write = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)


class EditForm(forms.Form):
  groups = Group.objects.all()
  types = []

  for gr in groups:
    types.append((gr.name,gr.name))

  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.ModelChoiceField(Group.objects.all())
  read = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)
  write = forms.ModelMultipleChoiceField(Project.objects.all(), required=False)


class ChangePassForm(forms.Form):
  """TODO: Docstring"""

  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  password_again = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())

  def clean(self):
    # rely on 'required' check to kick in
    if not self.cleaned_data.get('password'):
      return self.cleaned_data

    # rely on 'required' check to kick in
    if not self.cleaned_data.get('password_again'):
      return self.cleaned_data

    if self.cleaned_data['password'] == self.cleaned_data['password_again']:
      return self.cleaned_data

    del self.cleaned_data['password']
    del self.cleaned_data['password_again']

    raise forms.ValidationError("The entered passwords are not the same")


class CreateUser(handler.Handler):
  """Handler to handle user requests"""
  
  def getPostForm(self):
    return UserForm(self.POST)
  
  def getGetForm(self):
    return UserForm()

  def post(self):
    login = self.cleaned_data['login']
    firstname = self.cleaned_data['firstname']
    lastname = self.cleaned_data['lastname']
    password = self.cleaned_data['password']
    type = self.cleaned_data['type']
    read_projs = self.cleaned_data.get('read', [])
    write_projs = self.cleaned_data.get('write', [])

    user_logic.handle_add_user(login, firstname, lastname, password, type, read_projs, write_projs)

    return http.HttpResponseRedirect('./home')

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/new.html', dictionary=context)
    return http.HttpResponse(content)


class EditUser(handler.Handler):
  """Handler to handle the edits of a user"""
  
  def getPostForm(self):
    return EditForm(self.POST)

  def getGetForm(self):
    user_id = self.kwargs['user_id']
    user = User.objects.filter(id=user_id).get()
    groups = user.groups.all()
    profile = user_profile_logic.getProfile(user)

    initial = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'type': groups[0].id if groups else '',
        'read': [i.id for i in profile.read.all()],
        'write': [i.id for i in profile.write.all()],
        }

    return EditForm(initial=initial)

  def post(self):
    user_id = self.kwargs['user_id']
    rfirst_name = self.cleaned_data['firstname']
    rlast_name = self.cleaned_data['lastname']
    rtype = self.cleaned_data['type']
    read_projs = self.cleaned_data.get('read', [])
    write_projs = self.cleaned_data.get('write', [])

    user_logic.handle_edit(rfirst_name, rlast_name, rtype, user_id, read_projs, write_projs)

    return http.HttpResponseRedirect('../home')

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/edit.html', dictionary=context)
    return http.HttpResponse(content)


class Home(handler.Handler):
  """Handler to handle the user views"""
  
  def post(self):
    return http.HttpResponseRedirect('../home')
    
  def get(self):
    context = self.getContext()
    users = User.objects.all()

    result = [(i, user_profile_logic.getProfile(i)) for i in users]

    context['users'] = result

    content = loader.render_to_string('user/home.html', dictionary=context)
    return http.HttpResponse(content)


class PassChange(handler.Handler):
  """Handler to handle the change password requests"""

  def authenticated_disabled(self):
    context = self.getUserAuthenticationContext()
    user = self.user
    return context['is_beheerder']

  def getGetForm(self):
    return ChangePassForm()

  def getPostForm(self):
    return ChangePassForm(self.POST)

  def post(self):
    user_id = self.kwargs['user_id']
    password = self.cleaned_data['password']

    user_logic.handle_pass_change(user_id, password)
    return http.HttpResponseRedirect('../home')

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/change.html', dictionary=context)
    return http.HttpResponse(content)
