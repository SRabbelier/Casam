import mimetypes
import time
import os

from django.conf import settings


def handle_uploaded_file(file, name):
  """TODO: Docstring
  """

  DATADIR = settings.DATADIR

  timestamp = time.time()
  fileNameOnly = "%d-%s" % (timestamp, file.name)
  location = DATADIR + "%d-%s" % (timestamp, file.name)
  destination = open(location, 'wb+') #wb+ is write binary

  for chunk in file.chunks():
      destination.write(chunk)

  destination.close()

  return location, fileNameOnly


def load_file(name):
  mime = mimetypes.MimeTypes()
  filename ='data/' + name

  if os.path.exists(filename) and os.path.isfile(filename):
    mimetype = mime.guess_type(filename)
    picture = open(filename,'rb')
    return mimetype, picture

  return None, None


