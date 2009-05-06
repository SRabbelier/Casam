from django import forms
from django import http
from django.template import loader

from casam.views import handler
from casam.logic import login as login_logic


class LoginForm(forms.Form):
  """TODO: Docstring """
  username = forms.CharField(max_length=30)
  password = forms.CharField(max_length=10, widget=forms.widgets.PasswordInput())


class Login(handler.Handler):
  """Handler to handle Login requests
  """

  def authenticated(self):
    return True

  def getPostForm(self):
    return LoginForm(self.POST)
  
  def getGetForm(self):
    return LoginForm()
  
  def post(self):
    rusername = self.cleaned_data['username']
    rpassword = self.cleaned_data['password']

    if login_logic.handle_login(rusername, rpassword, self.request):
      return http.HttpResponseRedirect(self.BASE_PATH)
    else:
      return http.HttpResponseRedirect(self.path + '?status=failed')

  def get(self):
    status = self.GET.get('status')
    context = self.getContext()
    context['failed'] = status == 'failed'
    content = loader.render_to_string('main/login.html', dictionary=context)

    return http.HttpResponse(content)


class Logout(handler.Handler):
  """Handler to handle Logout requests
  """

  def get(self):
    login_logic.handle_logout(self.request)

    return http.HttpResponseRedirect(self.BASE_PATH)
