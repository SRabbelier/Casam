import uuid
import tempfile
import os

from StringIO import StringIO

from django import http
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

from PIL import Image

from casam.logic import modified_image as modified_image_logic
from casam.models import OriginalImage
from casam.models import Bitmap
from casam.models import PDM
from casam.models import ModifiedImage
from casam.views import handler


class Error(Exception):
  pass


class ImageNotFound(Error):
  pass


class UnknownImageType(Error):
  pass


class OriginalImageHandler(object):
  """Handler for OriginalImages.
  """

  def getImageRecord(self, imageID):
    try:
      imageRecord = OriginalImage.objects.all().get(id = imageID)
    except OriginalImage.DoesNotExist:
      raise ImageNotFound('Image could not be found')

    return imageRecord

  def save(self, im, img_path):
    im.save(img_path)

  def suffix(self):
    return ".jpg"

  def contentType(self):
    return "image/jpeg"



class BitmapImageHandler(object):
  """Handler for Bitmaps.
  """

  def getImageRecord(self, imageID):
    try:
      imageRecord = Bitmap.objects.all().get(id = imageID)
    except Bitmap.DoesNotExist:
      raise ImageNotFound('Bitmap could not be found')

    return imageRecord

  def save(self, im, img_path):
    im.save(img_path,transparency=0)

  def suffix(self):
    return ".gif"

  def contentType(self):
    return 'image/gif'

 
class OverlayImageHandler(object):
  """Handler for Bitmaps.
  """

  def getImageRecord(self, imageID):
    try:
      imageRecord = PDM.objects.all().get(id = imageID)
    except PDM.DoesNotExist:
      raise ImageNotFound('Overlay could not be found')

    return imageRecord

  def save(self, im, img_path):
    im.save(img_path)

  def suffix(self):
    return ".png"

  def contentType(self):
    return 'image/png'  



class ImageHandler(handler.Handler):
  """Base class to handle Image manipulation requests.
  """

  def getHandler(self):
    """Returns the handler for the type of the current request.
    """

    actions = {
        'original': OriginalImageHandler,
        'bitmap': BitmapImageHandler,
        'overlay': OverlayImageHandler,
        }

    img_type = self.kwargs.get('img_type')

    if img_type not in actions:
      raise UnknownImageType("No such image type '%s'." % img_type)

    handler_type = actions[img_type]
    return handler_type()

  def getImage(self):
    """Returns the path of the image for the current request.
    """

    img_type = self.kwargs.get('img_type')
    imageID = self.kwargs.get('uuid')
    handler= self.getHandler()

    imageRecord = handler.getImageRecord(imageID)

    transformation = self.infix()
    modim = modified_image_logic.getModifiedImage(imageRecord, transformation)

    img_name = modim.id + handler.suffix()
    img_path = os.path.join(tempfile.gettempdir(), img_name)

    #though the file already exists on the server, save it in temp to make sure it is jpeg
    if (not os.path.exists(img_path)) or img_type=='bitmap':
      location = os.path.join(self.DATA_DIR, imageRecord.id + '.gif')
      im = Image.open(location)
      im = im.convert("RGBA")

      self.save(im, img_path)

    return img_path

  def save(self, im, img_path):
    handler = self.getHandler()
    handler.save(im, img_path)

  def response(self, img_path):
    wrapper = FileWrapper(file(img_path, "rb"))
    handler = self.getHandler()
    content_type = handler.contentType()

    response = http.HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(img_path)

    return response

  def get(self):
    img_path = self.getImage()

    return self.response(img_path)


class SimpleHandler(ImageHandler):
  """
  """

  def infix(self):
    return "_simple"


class RatioHandler(ImageHandler):
  """
  """

  def infix(self):
    return "_byRatio_" + self.kwargs.get('img_ratio')

  def save(self, im, img_path):
    ratio = self.kwargs.get('img_ratio')

    floatRatio = float(ratio)

    #safeguard for not killing the server
    if floatRatio>=150:
      floatRatio = float(150)

    #resize the image with the correct ratio
    imageWidth = im.size[0] * (floatRatio/100)
    imageHeight = im.size[1] * (floatRatio/100)

    img_type = self.kwargs.get('img_type')
    if img_type == 'bitmap':
      newImage = im.resize((imageWidth,imageHeight),Image.NEAREST)
    else :
      newImage = im.resize((imageWidth,imageHeight),Image.ANTIALIAS)

    newImage.save(img_path)


class WidthHandler(ImageHandler):
  """
  """

  def infix(self):
    return "_byRatio_" + self.kwargs.get('img_width')

  def save(self, im, img_path):
    width = self.kwargs.get('img_width')
    floatWidth = float(width)

    #safeguard for not killing the server
    if floatWidth>=im.size[0]:
      floatWidth = float(im.size[0])

    #calculate the height corresponding to the given width
    imageHeight = im.size[1] * (floatWidth/im.size[0])

    img_type = self.kwargs.get('img_type')
    if img_type == 'bitmap':
      newImage = im.resize((floatWidth,floatHeight),Image.NEAREST)
    else :
      newImage = im.resize((floatWidth,floatHeight),Image.ANTIALIAS)

    #Save the image and put it in the request
    newImage.save(img_path)


class WidthHeightHandler(ImageHandler):
  """
  """

  def save(self, im, img_path):
    width = self.kwargs.get('img_width')
    height = self.kwargs.get('img_height')

    floatWidth = float(width)
    floatHeight = float(height)

    fullImageWidth = im.size[0]
    fullImageHeight = im.size[1]

    #initialize the values that will be altered in the following if statement
    resizeWidth = 0
    resizeHeight = 0

    if self.resizeByWidth(floatWidth, fullImageWidth, floatHeight, fullImageHeight):
      #Resize by resizing the width
      resizeRate = floatWidth / fullImageWidth
      resizeWidth = floatWidth
      resizeHeight = fullImageHeight * resizeRate
    else:
      #Resize by resizing the height
      resizeRate = floatHeight / fullImageHeight
      resizeWidth = fullImageWidth * resizeRate
      resizeHeight = floatHeight

    img_type = self.kwargs.get('img_type')
    if img_type == 'bitmap':
      newImage = im.resize((resizeWidth,resizeHeight),Image.NEAREST)
    else :
      newImage = im.resize((resizeWidth,resizeHeight),Image.ANTIALIAS)

    handler = self.getHandler()
    handler.save(newImage, img_path)


class MaxWidthHeightHandler(WidthHeightHandler):
  def infix(self):
    return "_byMaxWidthHeight_" + self.kwargs.get('img_width') + "_" + self.kwargs.get('img_height')

  def resizeByWidth(self, floatWidth, fullImageWidth, floatHeight, fullImageHeight):
    return (floatWidth / fullImageWidth) < (floatHeight / fullImageHeight)


class MinWidthHeightHandler(WidthHeightHandler):
  def infix(self):
    return "_byMinWidthHeight_" + self.kwargs.get('img_width') + "_" + self.kwargs.get('img_height')

  def resizeByWidth(self, floatWidth, fullImageWidth, floatHeight, fullImageHeight):
    return (floatWidth / fullImageWidth) > (floatHeight / fullImageHeight)


class ThumbnailHandler(ImageHandler):
  """
  """

  def infix(self):
    return "_thumbnail_" + self.kwargs.get('img_size')

  def save(self, im, img_path):
    widthandheight = self.kwargs.get('img_size')

    floatWidthAndHeight = float(widthandheight)

    fullImageWidth = im.size[0]
    fullImageHeight = im.size[1]
    squareSize = min(fullImageWidth, fullImageHeight)

    c1 = (fullImageWidth - squareSize) / 2
    c2 = (fullImageHeight - squareSize) / 2
    c3 = (fullImageWidth - squareSize) / 2 + squareSize
    c4 = (fullImageHeight - squareSize)/ 2 + squareSize
    box = (c1, c2, c3, c4)

    im = im.crop(box)

    img_type = self.kwargs.get('img_type')
    if img_type == 'bitmap':
      newImage = im.resize((floatWidthAndHeight,floatWidthAndHeight),Image.NEAREST)
    else :
      newImage = im.resize((floatWidthAndHeight,floatWidthAndHeight),Image.ANTIALIAS)

    #Save the image and put it in the request
    newImage.save(img_path)
