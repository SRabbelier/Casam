from casam.models import UserProfile
from casam.models import Project

from django.contrib.auth.models import User, Group


def handle_add_user(rlogin, rfirstname, rlastname, rpass, rtype, read_projs, write_projs):
  """TODO: Docstring
  """

  user = User.objects.create_user(rlogin,'',rpass)
  user.first_name = rfirstname
  user.last_name = rlastname
  user.is_staff = True
  user.set_password(rpass)


def handle_edit(rfirst_name, rlast_name, rtype, rid, rread, rwrite):
  """TODO: Docstring
  """

  user = User.objects.get(id=rid)
  user.first_name = rfirst_name
  user.last_name = rlast_name
  user.save()


def handle_pass_change(user_id, password):
  """TODO: Docstring
  """

  user = User.objects.get(id=user_id)
  user.set_password(password)
