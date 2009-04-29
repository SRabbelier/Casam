from django.contrib.auth.models import User, Group

from casam.models import Project
from casam.logic import user_profile as user_profile_logic


def handle_add_user(rlogin, rfirstname, rlastname, rpass, rtype, read_projs, write_projs):
  """TODO: Docstring
  """

  user = User.objects.create_user(rlogin,'',rpass)
  user.first_name = rfirstname
  user.last_name = rlastname
  user.is_staff = True
  user.set_password(rpass)
  user.groups = [rtype]
  user.save()

  user_profile_logic.handle_save_user_profile(user, read_projs, write_projs)


def handle_edit(rfirst_name, rlast_name, rtype, rid, read_projs, write_projs):
  """TODO: Docstring
  """

  user = User.objects.get(id=rid)
  user.first_name = rfirst_name
  user.last_name = rlast_name
  user.groups = [rtype]
  user.save()

  user_profile_logic.handle_save_user_profile(user, read_projs, write_projs)


def handle_pass_change(user_id, password):
  """TODO: Docstring
  """

  user = User.objects.get(id=user_id)
  user.set_password(password)
