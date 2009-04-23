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
    
  types=(('C', 'Chirurg'),('O', 'Onderzoeker'), ('A', 'Beheerder'))

  login = forms.CharField(max_length=30)
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.CharField(max_length=1, widget=forms.Select(choices=types))
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  read = forms.CharField(widget=forms.widgets.SelectMultiple(choices=choices))
  
class EditForm(forms.Form):
  types=(('C', 'Chirurg'),('O', 'Onderzoeker'), ('A', 'Beheerder'))
  
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.CharField(max_length=1, widget=forms.Select(choices=types))
  
  id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(), required=False)  
  
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
    read_projs = self.cleaned_data['read']
    user_logic.handle_add_user(login, firstname, lastname, password, type, read_projs)
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
  
class Edit(handler.Handler):
  """Handler to handle the edits of a user"""
  
  def getPostForm(self):
    user = User.objects.get(id=self.POST['id'])
    rfirst_name = user.first_name
    rlast_name= user.last_name
    rlogin = user.username
    rid = user.id
    initial = {'firstname': rfirst_name, 'lastname': rlast_name , 'login': rlogin, 'id': rid}
    return EditForm(initial = initial)
  
  def getGetForm(self):
    return http.HttpResponseRedirect('../home')
  
  def post(self):
    return http.HttpResponseRedirect('./home')
  
  def get(self):    
    context = self.getContext()
    user = context['USER']
    if user.is_authenticated():
      context['form'] = self.form
      content = loader.render_to_string('user/edit.html', dictionary=context)
      return http.HttpResponse(content)
    else:
      return http.HttpResponseRedirect(context['BASE_PATH'])
  
class Save(handler.Handler):
  """Handler to handle the saving of the edited user"""
  
  def post(self):
    return http.HttpResponseRedirect('../home')
  
  def get(self):
    rfirst_name = self.POST['firstname']
    rlast_name = self.POST['lastname']
    rtype = self.POST['type']
    rid = self.POST['id']
    return user_logic.handle_edit(rfirst_name, rlast_name, rtype, rid)


def home(request):
  user = request.user
  if user.is_authenticated():
    DATADIR = '../'+getattr(settings, 'DATADIR')
    users = User.objects.all()
  
    #groups = []
  
    #for us in users:
    #  groups.append(us.groups.all().get().name)
      
    #print groups
  
    #context = {'users':users, 'groups': groups, 'DATADIR':DATADIR}
    context = {'users': users, 'DATADIR': DATADIR}
  
    content = loader.render_to_string('user/home.html', dictionary=context)
    return http.HttpResponse(content)
  else:
    return http.HttpResponseRedirect(getattr(settings, 'DATADIR'))

def logout(request):
  return user_logic.handle_logout(request)
  
  