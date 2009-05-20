import uuid
import tempfile
import os

from StringIO import StringIO

from django import http
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

from PIL import Image

from casam.models import OriginalImage
from casam.models import Bitmap
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


class ImageHandler(handler.Handler):
  """Base class to handle Image manipulation requests.
  """

  def getHandler(self):
    """Returns the handler for the type of the current request.
    """

    actions = {
        'original': OriginalImageHandler,
        'bitmap': BitmapImageHandler,
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

    img_name = imageID + self.infix() + handler.suffix()
    img_path = os.path.join(tempfile.gettempdir(), img_name)

    #though the file already exists on the server, save it in temp to make sure it is jpeg
    if not os.path.exists(img_path):
      location = os.path.join(self.DATA_DIR, imageRecord.path)
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

    newImage = im.resize((floatWidth,imageHeight),Image.ANTIALIAS)

    #Save the image and put it in the request
    newImage.save(img_path)


class MaxWidthHeightHandler(handler.Handler):
  def get(self):
    width = self.kwargs.get('img_width')
    height = self.kwargs.get('img_height')
    imageID = self.kwargs.get('uuid')
    img_type = self.kwargs.get('img_type')

    floatWidth = float(width)
    floatHeight = float(height)

    if img_type == 'original':
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMaxWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".jpg"
    else:
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMaxWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".gif"

    #image was not found in cache, create it!
    if not os.path.exists(temporaryImage):
      if img_type == 'original':
        try:
          imageRecord = OriginalImage.objects.all().get(id = imageID)
        except OriginalImage.DoesNotExist:
          print 'Image could not be found'
      else:
        try:
          imageRecord = Bitmap.objects.all().get(id = imageID)
        except Bitmap.DoesNotExist:
          print 'Bitmap could not be found'

      location = "./" + self.DATA_DIR + "%s" % (imageRecord.path)
      im = Image.open(location)
      im = im.convert("RGBA")

      fullImageWidth = im.size[0]
      fullImageHeight = im.size[1]

      #initialize the values that will be altered in the following if statement
      resizeWidth = 0
      resizeHeight = 0

      if (floatWidth / fullImageWidth) < (floatHeight / fullImageHeight):
        #Resize by resizing the width
        resizeRate = floatWidth / fullImageWidth
        resizeWidth = floatWidth
        resizeHeight = fullImageHeight * resizeRate
      else:
        #Resize by resizing the height
        resizeRate = floatHeight / fullImageHeight
        resizeWidth = fullImageWidth * resizeRate
        resizeHeight = floatHeight

      newImage = im.resize((resizeWidth,resizeHeight),Image.ANTIALIAS)

      #Save the image and put it in the request
      if img_type == 'bitmap':
        newImage.save(temporaryImage,transparency=0)
      else:
        newImage.save(temporaryImage)

    #Put the image in the request
    wrapper = FileWrapper(file(temporaryImage, "rb"))
    if img_type == 'original':
      response = http.HttpResponse(wrapper,content_type='image/jpeg')
    else:
      response = http.HttpResponse(wrapper,content_type='image/gif')
    response['Content-Length'] = os.path.getsize(temporaryImage)

    return response


class MinWidthHeightHandler(handler.Handler):
  def get(self):
    width = self.kwargs.get('img_width')
    height = self.kwargs.get('img_height')
    imageID = self.kwargs.get('uuid')
    img_type = self.kwargs.get('img_type')

    floatWidth = float(width)
    floatHeight = float(height)

    if img_type == 'original':
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMinWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".jpg"
    else:
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMinWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".gif"

    #image was not found in cache, create it!
    if not os.path.exists(temporaryImage):
      if img_type == 'original':
        try:
          imageRecord = OriginalImage.objects.all().get(id = imageID)
        except OriginalImage.DoesNotExist:
          print 'Image could not be found'
      else:
        try:
          imageRecord = Bitmap.objects.all().get(id = imageID)
        except Bitmap.DoesNotExist:
          print 'Bitmap could not be found'
  
      location = "./" + self.DATA_DIR + "%s" % (imageRecord.path)
      im = Image.open(location)
      im = im.convert("RGB")

      fullImageWidth = im.size[0]
      fullImageHeight = im.size[1]

      #initialize the values that will be altered in the following if statement
      resizeWidth = 0
      resizeHeight = 0

      if (floatWidth / fullImageWidth) > (floatHeight / fullImageHeight):
        #Resize by resizing the width
        resizeRate = floatWidth / fullImageWidth
        resizeWidth = floatWidth
        resizeHeight = fullImageHeight * resizeRate

      else:
        #Resize by resizing the height
        resizeRate = floatHeight / fullImageHeight
        resizeWidth = fullImageWidth * resizeRate
        resizeHeight = floatHeight

      newImage = im.resize((resizeWidth,resizeHeight),Image.ANTIALIAS)

      #Save the image and put it in the request
      newImage.save(temporaryImage)

    #Put the image in the request
    wrapper = FileWrapper(file(temporaryImage, "rb"))
    if img_type == 'original':
      response = http.HttpResponse(wrapper,content_type='image/jpeg')
    else:
      response = http.HttpResponse(wrapper,content_type='image/gif')
    response['Content-Length'] = os.path.getsize(temporaryImage)

    return response


class ThumbnailHandler(handler.Handler):
  def get(self):
    img_type = self.kwargs.get('img_type')
    widthandheight = self.kwargs.get('img_size')
    imageID = self.kwargs.get('uuid')

    floatWidthAndHeight = float(widthandheight)

    if img_type == 'original':
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_thumbnail_" + str(floatWidthAndHeight) + ".jpg"
    else:
      temporaryImage = tempfile.gettempdir() + "/" + imageID + "_thumbnail_" + str(floatWidthAndHeight) + ".gif"

    #image was not found in cache, create it!
    if not os.path.exists(temporaryImage):
      if img_type == 'original':
        try:
          imageRecord = OriginalImage.objects.all().get(id = imageID)
        except OriginalImage.DoesNotExist:
          print 'Image could not be found'
      else:
        try:
          imageRecord = Bitmap.objects.all().get(id = imageID)
        except Bitmap.DoesNotExist:
          print 'Bitmap could not be found'

      location = "./" + self.DATA_DIR + "%s" % (imageRecord.path)
      fullImage = Image.open(location)
      fullImage = fullImage.convert("RGB")

      fullImageWidth = fullImage.size[0]
      fullImageHeight = fullImage.size[1]
      squareSize = min(fullImageWidth, fullImageHeight)

      c1 = (fullImageWidth - squareSize) / 2
      c2 = (fullImageHeight - squareSize) / 2
      c3 = (fullImageWidth - squareSize) / 2 + squareSize
      c4 = (fullImageHeight - squareSize)/ 2 + squareSize
      box = (c1, c2, c3, c4)

      im = fullImage.crop(box)

      newImage = im.resize((floatWidthAndHeight,floatWidthAndHeight),Image.ANTIALIAS)

      #Save the image and put it in the request
      newImage.save(temporaryImage)

    #Put the image in the request
    wrapper = FileWrapper(file(temporaryImage, "rb"))
    if img_type == 'original':
      response = http.HttpResponse(wrapper,content_type='image/jpeg')
    else:
      response = http.HttpResponse(wrapper,content_type='image/gif')
    response['Content-Length'] = os.path.getsize(temporaryImage)
  
    return response
