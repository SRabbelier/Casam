import uuid

from django import http
from django.template import loader
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

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
    
  types=(('C', 'Chirurg'),('O', 'Onderzoeker'), ('A', 'Beheerder'))

  login = forms.CharField(max_length=30)
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.CharField(max_length=1, widget=forms.Select(choices=types))
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  #id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(), required=False)
  #read = forms.CharField(widget=forms.widgets.SelectMultiple(choices=choices))
  
class LoginForm(forms.Form):
  """TODO: Docstring """
  username = forms.CharField(max_length=30)
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  
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
    user_logic.handle_add_user(login, firstname, lastname, password, type)
    return http.HttpResponseRedirect('./home')

  def get(self):
    context = self.getContext()
    context['form'] = self.form
    content = loader.render_to_string('user/new.html', dictionary=context)
    return http.HttpResponse(content)

class Login(handler.Handler):
  """Handler to handle Login requests"""
  
  def getPostForm(self):
    return LoginForm(self.POST)
  
  def getGetForm(self):
    return LoginForm()
  
  def post(self):
    #return user_logic.handle_login(self.cleaned_data['username'], self.cleaned_data['password'])
    return user_logic.handle_login(self.request)

  def get(self):
    context = self.getContext()
    context['form'] = self.form
    content = loader.render_to_string('main/login.html', dictionary=context)
    return http.HttpResponse(content)  

def view(request, id_str):
  DATADIR = '../'+getattr(settings, 'DATADIR')
  id = id_str
  user = User.objects.get(id=id)
  initial = {'name': user.name, 'login': user.login, 'password': user.password, 'type': user.type, 'id': id}
  context = {'form': UserForm(initial=initial)}
  content = loader.render_to_string('user/edit.html', dictionary=context)
  return http.HttpResponse(content)

def home(request):
  DATADIR = '../'+getattr(settings, 'DATADIR')
  print request.session
  users = User.objects.all()
#  for us in users:
#    if us.type == 'O':
#      us.type = 'Onderzoeker'
#    elif us.type == 'C':
#      us.type = 'Chirurg'
#    else:
#      us.type = 'Beheerder'
  context = {'users':users, 'DATADIR':DATADIR}

  content = loader.render_to_string('user/home.html', dictionary=context)
  return http.HttpResponse(content)
    
  
  