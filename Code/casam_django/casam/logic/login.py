from django.contrib import auth


def handle_login(rusername, rpassword, request):
  """TODO: Docstring
  """

  user = auth.authenticate(username=rusername, password=rpassword)
  if user and user.is_active:
    auth.login(request, user)


def handle_logout(request):
  """TODO: Docstring
  """

  auth.logout(request)
