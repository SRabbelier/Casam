import uuid
import tempfile
import os

from django import http
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

from casam.models import OriginalImage
from PIL import Image
from StringIO import StringIO

def simple(request,imageID):
  DATADIR = settings.DATADIR
    

  temporaryImage = tempfile.gettempdir() + "/" + imageID + "_simple" +".jpg"

  #though the file already exists on the server, save it in temp to make sure it is jpeg
  if not os.path.exists(temporaryImage):
    imageRecord = OriginalImage.objects.all().get(id = imageID)
    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
    im.save(temporaryImage)

    
  wrapper = FileWrapper(file(temporaryImage))
  response = http.HttpResponse(wrapper,content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response

def byRatio(request,ratio,imageID):
  DATADIR = settings.DATADIR
  
  floatRatio = float(ratio)

  temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byRatio_" + str(floatRatio) +".jpg"
  
  #image was not found in cache, create it!
  if not os.path.exists(temporaryImage):

    imageRecord = OriginalImage.objects.all().get(id = imageID)
    
    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
    
    #safeguard for not killing the server
    if floatRatio>=150:
      floatRatio = float(150)
  
    #resize the image with the correct ratio
    imageWidth = im.size[0] * (floatRatio/100)
    imageHeight = im.size[1] * (floatRatio/100)
    
    newImage = im.resize((imageWidth,imageHeight),Image.ANTIALIAS)
    
    newImage.save(temporaryImage)

  #Put the image in the request
  wrapper = FileWrapper(file(temporaryImage))
  response = http.HttpResponse(wrapper, content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response


def byWidth(request,width,imageID):
  DATADIR = settings.DATADIR
  
  floatWidth = float(width)

  temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byWidth_" + str(floatWidth) +".jpg"

  #image was not found in cache, create it!
  if not os.path.exists(temporaryImage):
    
    imageRecord = OriginalImage.objects.all().get(id = imageID)

    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
  
    
    #safeguard for not killing the server
    if floatWidth>=im.size[0]:
      floatWidth = float(im.size[0])
  
    #calculate the height corresponding to the given width
    imageHeight = im.size[1] * (floatWidth/im.size[0])
    
    newImage = im.resize((floatWidth,imageHeight),Image.ANTIALIAS)
  
    #Save the image and put it in the request
    newImage.save(temporaryImage)
    
  #Put the image in the request
  wrapper = FileWrapper(file(temporaryImage))
  response = http.HttpResponse(wrapper, content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response

def byMaxWidthHeight(request,width,height,imageID):
  DATADIR = settings.DATADIR
  
  floatWidth = float(width)
  floatHeight = float(height)

  temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMaxWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".jpg"

  #image was not found in cache, create it!
  if not os.path.exists(temporaryImage):
    
    imageRecord = OriginalImage.objects.all().get(id = imageID)

    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
  
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
    newImage.save(temporaryImage)
    
  #Put the image in the request
  wrapper = FileWrapper(file(temporaryImage))
  response = http.HttpResponse(wrapper, content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response

def byMinWidthHeight(request,width,height,imageID):
  DATADIR = settings.DATADIR
  
  floatWidth = float(width)
  floatHeight = float(height)

  temporaryImage = tempfile.gettempdir() + "/" + imageID + "_byMinWidthHeight_" + str(floatWidth) + "_" + str(floatHeight) +".jpg"

  #image was not found in cache, create it!
  if not os.path.exists(temporaryImage):
    
    imageRecord = OriginalImage.objects.all().get(id = imageID)

    location = "./" + DATADIR + "%s" % (imageRecord.path)
    im = Image.open(location)
  
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
  wrapper = FileWrapper(file(temporaryImage))
  response = http.HttpResponse(wrapper, content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response

def thumbnail(request,widthandheight,imageID):
  DATADIR = settings.DATADIR
  
  floatWidthAndHeight = float(widthandheight)

  temporaryImage = os.path.join(tempfile.gettempdir(), 
      imageID + "_thumbnail_" + str(floatWidthAndHeight) + ".jpg")

  #image was not found in cache, create it!
  if not os.path.exists(temporaryImage):
    imageRecord = OriginalImage.objects.all().get(id = imageID)

    location = "./" + DATADIR + "%s" % (imageRecord.path)
    fullImage = Image.open(location)
    
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
  content = open(temporaryImage, 'rb')
  response = http.HttpResponse(content, content_type='image/jpeg')
  response['Content-Length'] = os.path.getsize(temporaryImage)

  return response
