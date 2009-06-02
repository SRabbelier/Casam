import uuid

from django.conf import settings

from PIL import Image

from casam.logic import fileupload as fileupload_logic
from casam.models import Project
from casam.models import OriginalImage


def handle_uploaded_image(file, name, id_str):
  """TODO: Docstring
  """
  
  #save the uploaded image
  proj = Project.objects.get(id=id_str)

  properties = dict(
      name=name,
      project=proj,
      )

  oi = OriginalImage(**properties)
  oi.save()

  file_name = oi.id + '.jpg'
  fileupload_logic.handle_uploaded_file(file, file_name)

  return oi
