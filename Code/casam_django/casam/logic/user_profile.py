from casam.models import UserProfile


def handle_save_user_profile(user, read_projects, write_projects):
  """TODO: Docstring
  """

  try:
    profile = user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile(user=user)
    profile.save()

  profile.read = read_projects
  profile.write = write_projects
  profile.save()
