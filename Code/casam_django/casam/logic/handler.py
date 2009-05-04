from casam.models import UserProfile
from django.contrib.auth.models import Group

def getProfile(user):
  """TODO: Docstring
  """

  if not user.is_authenticated():
    return None

  try:
    prof = user.get_profile()
  except UserProfile.DoesNotExist:
    prof = UserProfile(user=user)
    prof.save()
  return prof


def getType(user):
  """TODO: Docstring
  """

  if not user.is_authenticated():
    return ''

  try:
    rtype = user.groups.all().get()
  except Group.DoesNotExist:
    return ''

  return str(rtype)
