import mimetypes
import time
import os

from django.conf import settings


def handle_uploaded_file(file, name):
  """TODO: Docstring
  """

  DATADIR = settings.DATADIR

  location = os.path.join(DATADIR, name)
  destination = open(location, 'wb+') #wb+ is write binary

  for chunk in file.chunks():
      destination.write(chunk)

  destination.close()

  return location


def load_file(name):
  mime = mimetypes.MimeTypes()

  DATADIR = settings.DATADIR

  location = os.path.join(DATADIR, name)

  if os.path.exists(location) and os.path.isfile(location):
    mimetype, _ = mime.guess_type(location)
    file = open(location,'rb')
    return mimetype, file

  return None, None
