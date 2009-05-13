from django.contrib import auth
import datetime

def handle_login(rusername, rpassword, rexpiration, request):
  """TODO: Docstring
  """

  user = auth.authenticate(username=rusername, password=rpassword)
  if user and user.is_active:
    auth.login(request, user)
    expiration = int(rexpiration)
    #Don't ask but it must be a timedelta object...
    #request.session.set_expiry(expiration)
    request.session.set_expiry(datetime.timedelta(0,expiration))
    return True

  return False


def handle_logout(request):
  """TODO: Docstring
  """

  auth.logout(request)
