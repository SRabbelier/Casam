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
  
class LoginForm(forms.Form):
  """TODO: Docstring """
  username = forms.CharField(max_length=30)
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  
class ChangePassForm(forms.Form):
  """TODO: Docstring"""
  login = forms.CharField(max_length=10, widget=forms.widgets.TextInput(attrs={'readonly': 'readonly'}))
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  password2 = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput(), label="Password (again)")
  id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(attrs={'readonly': 'readonly'}))  
  
class Users(handler.Handler):
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


class Login(handler.Handler):
  """Handler to handle Login requests"""

  def authenticated(self):
    return True

  def getPostForm(self):
    return LoginForm(self.POST)
  
  def getGetForm(self):
    return LoginForm()
  
  def post(self):
    #return user_logic.handle_login(self.cleaned_data['username'], self.cleaned_data['password'])
    return user_logic.handle_login(self.request)

  def get(self):
    context = self.getContext()
    content = loader.render_to_string('main/login.html', dictionary=context)
    return http.HttpResponse(content)  
  
class Edit(handler.Handler):
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
    return http.HttpResponseRedirect('../home')
  
  def post(self):
    return http.HttpResponseRedirect('./home')
  
  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/edit.html', dictionary=context)
    return http.HttpResponse(content)

class Save(handler.Handler):
  """Handler to handle the saving of the edited user"""
  
  def post(self):
    return http.HttpResponseRedirect('../home')
  
  def get(self):
    rfirst_name = self.POST['firstname']
    rlast_name = self.POST['lastname']
    rtype = self.POST['type']
    rid = self.POST['id']
    rread = self.POST.getlist('read')
    rwrite = self.POST.getlist('write')

    return user_logic.handle_edit(rfirst_name, rlast_name, rtype, rid, rread, rwrite)

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
  
  def getPostForm(self):
    context = self.getUserAuthenticationContext()
    user = self.user
    if context['is_beheerder']:
      print self.POST
      user = User.objects.get(id=self.POST['id'])
      rlogin = user.username
      rid = self.POST['id']
      initial = {
          'login': rlogin,
          'id': rid,
          }
      return ChangePassForm(initial = initial)
    else:
      return http.HttpResponseRedirect(context['BASEPATH']+'user/home')       
  
  def getGetForm(self):
    return http.HttpResponseRedirect('../home')
  
  def post(self):
    return http.HttpResponseRedirect('./home')
  
  def get(self):
    context = self.getContext()
    content = loader.render_to_string('user/change.html', dictionary=context)
    return http.HttpResponse(content)

class Change(handler.Handler):
  """Handler to save the changed password"""
  
  def post(self):
    return http.HttpResponseRedirect('../home')
  
  def get(self):
    rlogin = self.POST['login']
    rpass1 = self.POST['password']
    rpass2 = self.POST['password2']
    rid = self.POST['id']
    
    if user_logic.handle_pass_change(rlogin, rpass1, rpass2, rid):
      return http.HttpResponseRedirect('./home')
    else:
      context = self.getContext()
      context['form'] = ChangePassForm(initial={'login': rlogin, 'id': rid})
      content = loader.render_to_string('user/change.html', dictionary=context)
      return http.HttpResponse(content)
