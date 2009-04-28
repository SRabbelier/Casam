import mimetypes
import time
import os

from django.conf import settings


def handle_uploaded_file(file, name):
  """TODO: Docstring
  """

  DATADIR = settings.DATADIR

  filename = file.name.replace(' ', '_')

  timestamp = time.time()
  fileNameOnly = "%d-%s" % (timestamp, filename)
  location = DATADIR + "%d-%s" % (timestamp, filename)
  destination = open(location, 'wb+') #wb+ is write binary

  for chunk in file.chunks():
      destination.write(chunk)

  destination.close()

  return location, fileNameOnly, timestamp


def load_file(name):
  mime = mimetypes.MimeTypes()
  filename ='data/' + name

  if os.path.exists(filename) and os.path.isfile(filename):
    mimetype = mime.guess_type(filename)
    picture = open(filename,'rb')
    return mimetype, picture

  return None, None


