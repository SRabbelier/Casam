from django import forms
from django import http
from django.template import loader

from casam.views import handler
from casam.logic import users as user_logic


class LoginForm(forms.Form):
  """TODO: Docstring """
  username = forms.CharField(max_length=30)
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())


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

