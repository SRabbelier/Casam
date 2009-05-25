from PIL import Image
from PIL import ImageDraw

from django.conf import settings

class PDMOverlay(object):
  '''
  Creates a visual representation of the Point Distribution model using PIL
  '''


  def __init__(self, size):
    '''
    '''

    self.image = Image.new('RGBA',size,(0,0,0,0))
    self.imageDraw = ImageDraw.Draw(self.image)
  
  def drawMeans(self, positions):
    '''
    Get a visual representation of the means at the given coordinates
    '''
    ellipsoidSize = self.image.size[0]/100 #size of the ellipsoids, dependent on width of image
    for position in range(len(positions)):
      coordinate = positions[position]
      xmin = coordinate[0] - ellipsoidSize
      xmax = coordinate[0] + ellipsoidSize
      ymin = coordinate[1] - ellipsoidSize
      ymax = coordinate[1] + ellipsoidSize
      self.imageDraw.ellipse((xmin,ymin,xmax,ymax), fill=(150,0,255))

  def drawVariations(self, positions):
    '''
    Get a visual representation of the variations at the given coordinates using lines
    '''
    for position in range(len(positions)/2):
      coordinate1 = positions[position*2]
      coordinate2 = positions[(position*2)+1]
      print coordinate1," and 2: " ,coordinate2
      x1 = coordinate1[0]
      x2 = coordinate2[0]
      y1 = coordinate1[1]
      y2 = coordinate2[1]

      self.imageDraw.line((x1,y1,x2,y2), fill=(255,0,150))
    
  def saveImage(self,path):
    '''
    Save the image as a transparant png to the datadir???
    ''' 
    #TODO flip the image vertically to compensate for inverted y-coordinates in VTK
    self.image.save(path,"PNG")
    
    
