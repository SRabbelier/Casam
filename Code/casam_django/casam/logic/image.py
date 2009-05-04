import uuid

from django.conf import settings

from PIL import Image

from casam.logic import fileupload as fileupload_logic
from casam.models import Patient
from casam.models import Project
from casam.models import OriginalImage


def handle_crop_image(file, location, timestamp):
  """TODO: Docstring
  """

  #open the file and create a thumbnail out of it
  fullImage = Image.open(location)
  fullImageWidth = fullImage.size[0]
  fullImageHeight = fullImage.size[1]
  squareSize = min(fullImageWidth, fullImageHeight)

  c1 = (fullImageWidth - squareSize) / 2
  c2 = (fullImageHeight - squareSize) / 2
  c3 = (fullImageWidth - squareSize) / 2 + squareSize
  c4 = (fullImageHeight - squareSize)/ 2 + squareSize
  box = (c1, c2, c3, c4)

  fullImage = fullImage.crop(box)

  sizes = 50,100,200,300

  for singleSize in sizes:
    thumbnailLocation = settings.DATADIR + "thumbnail/%d/%d-%s" % (
        singleSize,timestamp, file.name)

    thumbnail=fullImage.copy()
    thumbnail.thumbnail((singleSize,singleSize), Image.ANTIALIAS)
    thumbnail.save(thumbnailLocation)


def handle_uploaded_image(file, name, is_left, id_str):
  """TODO: Docstring
  """

  location, fileNameOnly, timestamp = fileupload_logic.handle_uploaded_file(file, name)
  #handle_crop_image(file, location, timestamp)

  #temporarly create a patient object
  #because we need this info
  Patient.objects.all()
  pat = Patient(corpse_id=234,sex=True)
  pat.save()
  #safe the uploaded image
  OriginalImage.objects.all()

  proj = Project.objects.get(id=id_str)

  properties = dict(
      patient=pat,
      name=name,
      path=fileNameOnly,
      is_left=is_left,
      project=proj,
      )

  oi = OriginalImage(**properties)
  oi.save()
  return oi
