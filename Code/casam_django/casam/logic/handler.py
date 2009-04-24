from casam.models import UserProfile
from django.contrib.auth.models import Group

def getProfile(user):
  try:
    prof = user.get_profile()
  except UserProfile.DoesNotExist:
    prof = UserProfile(user=user)
  return prof

def getType(user):
  try:
    rtype = user.groups.all().get()
  except Group.DoesNotExist:
    return ''
    
  return str(rtype)