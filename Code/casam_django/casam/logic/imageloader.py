import uuid
import tempfile
import os

from django import http
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

from casam.models import OriginalImage
from casam.models import Bitmap
from PIL import Image
from StringIO import StringIO

def simple(request,**kwargs):
  img_type = kwargs.get('img_type')
  imageID = kwargs.get('uuid')
  DATADIR = settings.DATADIR
    
  if img_type == 'original':
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_simple" +".jpg"
  else:
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_simple" +".gif"

  #though the file already exists on the server, save it in temp to make sure it is jpeg
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
    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
    im = im.convert("RGB")
    im.save(temporaryImage)

    
  wrapper = FileWrapper(file(temporaryImage, "rb"))
  if img_type == 'original':
    response = http.HttpResponse(wrapper,content_type='image/jpeg')
  else:
    response = http.HttpResponse(wrapper,content_type='image/gif')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response

def byRatio(request, **kwargs):
  img_type = kwargs.get('img_type')
  imageID = kwargs.get('uuid')
  ratio = kwargs.get('img_ratio')
  DATADIR = settings.DATADIR
  
  floatRatio = float(ratio)

  if img_type == 'original':
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byRatio_" + str(floatRatio) +".jpg"
  else:
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byRatio_" + str(floatRatio) +".gif"
  
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
    
    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
    im = im.convert("RGB")

    #safeguard for not killing the server
    if floatRatio>=150:
      floatRatio = float(150)
  
    #resize the image with the correct ratio
    imageWidth = im.size[0] * (floatRatio/100)
    imageHeight = im.size[1] * (floatRatio/100)
    
    newImage = im.resize((imageWidth,imageHeight),Image.ANTIALIAS)
    
    newImage.save(temporaryImage)

  #Put the image in the request
  wrapper = FileWrapper(file(temporaryImage, "rb"))
  if img_type == 'original':
    response = http.HttpResponse(wrapper,content_type='image/jpeg')
  else:
    response = http.HttpResponse(wrapper,content_type='image/gif')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response


def byWidth(request, **kwargs):
  width = kwargs.get('img_width')
  imageID = kwargs.get('uuid')
  img_type = kwargs.get('img_type')
  DATADIR = settings.DATADIR
  
  floatWidth = float(width)

  if img_type == 'original':
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byWidth_" + str(floatWidth) +".jpg"
  else:
    temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byWidth_" + str(floatWidth) +".gif"

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

    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
    im = im.convert("RGB")

    
    #safeguard for not killing the server
    if floatWidth>=im.size[0]:
      floatWidth = float(im.size[0])
  
    #calculate the height corresponding to the given width
    imageHeight = im.size[1] * (floatWidth/im.size[0])
    
    newImage = im.resize((floatWidth,imageHeight),Image.ANTIALIAS)
  
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

def byMaxWidthHeight(request, **kwargs):
  width = kwargs.get('img_width')
  height = kwargs.get('img_height')
  imageID = kwargs.get('uuid')
  img_type = kwargs.get('img_type')
  DATADIR = settings.DATADIR
  
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
    
    location = "./" + DATADIR + "%s" % (imageRecord.path)
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

def byMinWidthHeight(request, **kwargs):
  width = kwargs.get('img_width')
  height = kwargs.get('img_height')
  imageID = kwargs.get('uuid')
  img_type = kwargs.get('img_type')
  DATADIR = settings.DATADIR
  
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

    location = "./" + DATADIR + "%s" % (imageRecord.path)
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

def thumbnail(request, *args, **kwargs):
  img_type = kwargs.get('img_type')
  widthandheight = kwargs.get('img_size')
  imageID = kwargs.get('uuid')
  DATADIR = settings.DATADIR
  
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

    location = "./" + DATADIR + "%s" % (imageRecord.path)
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
