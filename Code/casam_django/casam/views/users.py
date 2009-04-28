import uuid

from django import http
from django.template import loader
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

from casam.logic import users as user_logic
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
  read = forms.ModelMultipleChoiceField(Project.objects.all())
  write = forms.ModelMultipleChoiceField(Project.objects.all())


class EditForm(forms.Form):
  groups = Group.objects.all()
  types = []
  
  for gr in groups:
    types.append((gr.name,gr.name))
  
  login = forms.CharField(max_length=10, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly'}))
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.ModelChoiceField(Group.objects.all())
  read = forms.ModelMultipleChoiceField(Project.objects.all())
  write = forms.ModelMultipleChoiceField(Project.objects.all())

  id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(attrs={'readonly': 'readonly'}))  


class ChangePassForm(forms.Form):
  """TODO: Docstring"""
  login = forms.CharField(max_length=10, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly'}))
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  password2 = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput(), label="Password (again)")
  id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(attrs={'readonly': 'readonly'}))

  def clean(self):
    if self.cleaned_data['password'] == self.cleaned_data['password2']:
      return self.cleaned_data

    del self.cleaned_data['password']
    del self.cleaned_data['password2']

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
    read_projs = self.cleaned_data['read']
    write_projs = self.cleaned_data['write']
    user_logic.handle_add_user(login, firstname, lastname, password, type, read_projs, write_projs)
    return http.HttpResponseRedirect('./home')

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/new.html', dictionary=context)
    return http.HttpResponse(content)


class EditUser(handler.Handler):
  """Handler to handle the edits of a user"""
  
  def getPostForm(self):
    context = self.getUserAuthenticationContext()
    user = User.objects.get(id=self.POST['id'])
    rfirst_name = user.first_name
    rlast_name= user.last_name
    rlogin = user.username
    rid = user.id
    rtype = user.groups.all().get()
    rread = [i.id for i in user.get_profile().read.all()]
    rwrite = [i.id for i in user.get_profile().write.all()]

    initial = {
        'firstname': rfirst_name,
        'lastname': rlast_name,
        'login': rlogin,
        'id': rid,
        'type': rtype.id,
        'read': rread,
        'write': rwrite,
        }

    return EditForm(initial = initial)

  def getGetForm(self):
    return EditForm()

  def post(self):
    rfirst_name = self.POST['firstname']
    rlast_name = self.POST['lastname']
    rtype = self.POST['type']
    rid = self.POST['id']
    rread = self.POST.getlist('read')
    rwrite = self.POST.getlist('write')

    return user_logic.handle_edit(rfirst_name, rlast_name, rtype, rid, rread, rwrite)
  
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

    context['users'] = users

    content = loader.render_to_string('user/home.html', dictionary=context)
    return http.HttpResponse(content)


def logout(request):
  return user_logic.handle_logout(request)


class PassChange(handler.Handler):
  """Handler to handle the change password requests"""

  def authenticated(self):
    context = self.getUserAuthenticationContext()
    user = self.user
    return context['is_beheerder']

  def getPostForm(self):
    user = User.objects.get(id=self.POST['id'])
    rlogin = user.username
    rid = self.POST['id']
    initial = {
        'login': rlogin,
        'id': rid,
        }
    return ChangePassForm(initial = initial)

  def getGetForm(self):
    return ChangePassForm()

  def post(self):
    rlogin = self.POST['login']
    rpass1 = self.POST['password']
    rpass2 = self.POST['password2']
    rid = self.POST['id']

    if user_logic.handle_pass_change(rlogin, rpass1, rpass2, rid):
      pass

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/change.html', dictionary=context)
    return http.HttpResponse(content)
