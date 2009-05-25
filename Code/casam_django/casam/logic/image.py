import uuid

from django.conf import settings

from PIL import Image

from casam.logic import fileupload as fileupload_logic
from casam.models import Project
from casam.models import OriginalImage


#def handle_uploaded_image(file, name, is_left, id_str):
def handle_uploaded_image(file, name, id_str):
  """TODO: Docstring
  """

  location, fileNameOnly = fileupload_logic.handle_uploaded_file(file, name)
  #handle_crop_image(file, location, timestamp)

  #save the uploaded image
  OriginalImage.objects.all()

  proj = Project.objects.get(id=id_str)

  properties = dict(
      name=name,
      path=fileNameOnly,
      project=proj,
      )

  oi = OriginalImage(**properties)
  oi.save()
  
  fileupload_logic.handle_uploaded_file(file, oi.id)

  return oi
