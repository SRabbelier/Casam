from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps


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
    ellipsoidSize = self.image.size[0]/250 #size of the ellipsoids, dependent on width of image
    for position in range(len(positions)):
      coordinate = positions[position]
      xmin = coordinate[0] - ellipsoidSize
      xmax = coordinate[0] + ellipsoidSize
      ymin = coordinate[1] - ellipsoidSize
      ymax = coordinate[1] + ellipsoidSize
      self.imageDraw.ellipse((xmin,ymin,xmax,ymax), fill=(50,205,50))#forest green
  #(34,139,34) Forest Green
  #(60,179,113) Medium Sea Green
  #(46,139,87) Sea Green
  def drawVariations(self, positions):
    '''
    Get a visual representation of the variations at the given coordinates using lines
    '''
    for position in range(len(positions)/2):
      #color first and second modes of variation differently
      if (position%2 == 0): #first mode of variation
        color=(255,00,0)#Medium Sea Green
      else:
        color = (255,69,71)#Sea Green
      coordinate1 = positions[position*2]
      coordinate2 = positions[(position*2)+1]
      x1 = coordinate1[0]
      x2 = coordinate2[0]
      y1 = coordinate1[1]
      y2 = coordinate2[1]
      self.imageDraw.line((x1,y1,x2,y2), fill=(color), width=5)
    
  def saveImage(self,path):
    '''
    Save the image as a transparant png to the supplied path
    ''' 
    self.image.save(path,"PNG")
    
    
