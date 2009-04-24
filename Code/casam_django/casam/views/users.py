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
  read = forms.MultipleChoiceField(choices=choices)
  write = forms.MultipleChoiceField(choices=choices)
  
class EditForm(forms.Form):
  groups = Group.objects.all()
  types = []
  
  for gr in groups:
    types.append((gr.name,gr.name))
  
  firstname = forms.CharField(max_length=30)
  lastname = forms.CharField(max_length=30)
  type = forms.ModelChoiceField(Group.objects.all())
  
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
    write_projs = self.cleaned_data['write']
    user_logic.handle_add_user(login, firstname, lastname, password, type, read_projs, write_projs)
    return http.HttpResponseRedirect('./home')

  def get(self):
    context = self.getContext()
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
    content = loader.render_to_string('main/login.html', dictionary=context)
    return http.HttpResponse(content)  
  
class Edit(handler.Handler):
  """Handler to handle the edits of a user"""
  
  def getPostForm(self):
    context = self.getUserAuthenticationContext()
    user = self.user
    if context['is_beheerder']:
      user = User.objects.get(id=self.POST['id'])
      rfirst_name = user.first_name
      rlast_name= user.last_name
      rlogin = user.username
      rid = user.id
      rtype = user.groups.all().get()
      
      teller = 1
      for gr in Group.objects.all():
        if rtype == gr:
          break
        else:
          teller += 1
           
      initial = {'firstname': rfirst_name, 'lastname': rlast_name , 'login': rlogin, 'id': rid, 'type': teller}
      return EditForm(initial = initial)
    else:
      return http.HttpResponseRedirect(context['BASEPATH']+'user/home')
  
  def getGetForm(self):
    return http.HttpResponseRedirect('../home')
  
  def post(self):
    return http.HttpResponseRedirect('./home')
  
  def get(self):    
    context = self.getContext()
    user = self.user
    if user.is_authenticated():
      if context['is_beheerder']:
        content = loader.render_to_string('user/edit.html', dictionary=context)
        return http.HttpResponse(content)
      else:
        return http.HttpResponseRedirect(context['BASE_PATH']+'user/home')
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

class Home(handler.Handler):
  """Handler to handle the user views"""
  
  def post(self):
    return http.HttpResponseRedirect('../home')
    
  def get(self):
    context = self.getContext()
    user = self.user
    if user.is_authenticated():
      if context['is_beheerder']:
        users = User.objects.all()
    
        context['users'] = users
      
        content = loader.render_to_string('user/home.html', dictionary=context)
        return http.HttpResponse(content)
      else:
        return http.HttpResponseRedirect(context['BASE_PATH']+'home')
    else:
      return http.HttpResponseRedirect(context['BASE_PATH'])

def logout(request):
  return user_logic.handle_logout(request)
  
  