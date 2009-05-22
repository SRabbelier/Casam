import Image
import ImageDraw

class PDMOverlay(object):
  '''
  Creates a visual representation of the Point Distribution model using PIL
  '''


  def __init__(self, size):
    '''
    '''

    size = (600,480)
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
    Get a visual representation of the variations at the given coordinates
    '''
    for position in range(len(positions)/2):
      coordinate1 = positions[position*2]
      coordinate2 = positions[(position*2)+1]
      x1 = coordinate1[0]
      x2 = coordinate2[0]
      y1 = coordinate1[1]
      y2 = coordinate2[1]
      self.imageDraw.line((x1,y1,x2,y2), fill=(255,0,150))
    
    
  def saveImage(self):
    self.image.save('test.png',"PNG")


def main():
  size = (600,480)
  positions = [(300,50),(50,130),(400,300),(450,320)]
  pdmo = PDMOverlay(size)
  pdmo.drawVariations(positions)
  pdmo.drawMeans(positions)
  pdmo.saveImage()

if __name__ == '__main__':
  main()

