from casam.models import UserProfile
from django.contrib.auth.models import Group

def getProfile(user):
  """TODO: Docstring
  """

  try:
    prof = user.get_profile()
  except UserProfile.DoesNotExist:
    prof = UserProfile(user=user)
    prof.save()
  return prof


def getType(user):
  """TODO: Docstring
  """

  try:
    rtype = user.groups.all().get()
  except Group.DoesNotExist:
    return ''

  return str(rtype)
