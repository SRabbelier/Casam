import uuid

from django import http
from django.template import loader
from django import forms
from django.conf import settings

from casam.models import OriginalImage
from casam.models import Project
from casam.models import ProjectMeasurementList
from casam.modelsls import Measurement
from casam.models import User

class UserForm(forms.Form):
  choices = []
  projects = Project.objects.all()

  for pr in projects:
    choices.append((pr.id,pr.name))

  login = forms.CharField(max_length=30)
  name = forms.CharField(max_length=100)
  type = forms.CharField(max_length=1, widget=forms.Select(choices=(('C', 'Chirurg'),('O', 'Onderzoeker'), ('A', 'Beheerder'))))
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())
  id = forms.CharField(max_length=40, widget=forms.widgets.HiddenInput(), required=False)
  read = forms.CharField(widget=forms.widgets.SelectMultiple(choices=choices))

def new(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      handle_add_user(request.POST)
      return http.HttpResponseRedirect('/')

  context = {'form': UserForm()}
  content = loader.render_to_string('user/new.html', dictionary=context)
  return http.HttpResponse(content)

def handle_add_user(post):
  user = User(login=post['login'], name=post['name'],type=post['type'],password='12345', id=post['id'])
  user.save()
  projid = uuid.UUID(post['read'])
  pr = Project.objects.get(id=projid)
  user.read.add(pr)
  print user.read.all()
  user.save()

def view(request, id_str):
  DATADIR = '../'+getattr(settings, 'DATADIR')
  id = uuid.UUID(id_str)
  user = User.objects.get(id=id)
  initial = {'name': user.name, 'login': user.login, 'password': user.password, 'type': user.type, 'id': id}
  context = {'form': UserForm(initial=initial)}
  content = loader.render_to_string('user/edit.html', dictionary=context)
  return http.HttpResponse(content)

def home(request):
  DATADIR = '../'+getattr(settings, 'DATADIR')
  users = User.objects.all()
  for us in users:
    if us.type == 'O':
      us.type = 'Onderzoeker'
    elif us.type == 'C':
      us.type = 'Chirurg'
    else:
      us.type = 'Beheerder'
  context = {'users':users, 'DATADIR':DATADIR}

  content = loader.render_to_string('user/home.html', dictionary=context)
  return http.HttpResponse(content)
