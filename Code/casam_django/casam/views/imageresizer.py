import uuid

from PIL import Image
from StringIO import StringIO
from django.conf import settings
from django import http
import tempfile
import os
from django.core.servers.basehttp import FileWrapper

def byRatio(request,ratio,imageFileName):
  user = request.user
  if user.is_authenticated():
    DATADIR = settings.DATADIR
    location = "./" + DATADIR + "%s" % (imageFileName)
    im = Image.open(location)
    
    floatRatio = float(ratio) 
    #safeguard for not killing the server
    if floatRatio>=100:
      floatRatio = float(100)
  
    #resize the image with the correct ratio
    imageWidth = im.size[0] * (floatRatio/100)
    imageHeight = im.size[1] * (floatRatio/100)
    
    newImage = im.resize((imageWidth,imageHeight))
    
    #Save the image and put it in the request
    __, temporaryImage = tempfile.mkstemp(suffix=".jpg")  
    newImage.save(temporaryImage)
    wrapper = FileWrapper(file(temporaryImage))
    response = http.HttpResponse(wrapper, content_type='image/jpeg')
    response['Content-Length'] = os.path.getsize(temporaryImage)
  
    return response
  else:
    return http.HttpResponseRedirect(getattr(settings, 'DATADIR'))

def byWidth(request,width,imageFileName):
  user = request.user
  if user.is_authenticated():  
    DATADIR = settings.DATADIR
    location = "./" + DATADIR + "%s" % (imageFileName)
    im = Image.open(location)
    
    floatWidth = float(width) 
    
    #safeguard for not killing the server
    if floatWidth>=im.size[0]:
      floatWidth = float(im.size[0])
  
    #calculate the height corresponding to the given width
    imageHeight = im.size[1] * (floatWidth/im.size[0])
    
    newImage = im.resize((floatWidth,imageHeight))
    
    #Save the image and put it in the request
    __, temporaryImage = tempfile.mkstemp(suffix=".jpg")  
    newImage.save(temporaryImage)
    wrapper = FileWrapper(file(temporaryImage))
    response = http.HttpResponse(wrapper, content_type='image/jpeg')
    response['Content-Length'] = os.path.getsize(temporaryImage)
  
    return response
  else:
    return http.HttpResponseRedirect(getattr(settings, 'DATADIR'))
