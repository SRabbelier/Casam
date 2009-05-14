from PIL import Image
from django.conf import settings
from casam.models import Bitmap
import time


def handle_bitmap_stream(dump,image_id,original_image):
  
  if dump.find("_scanline:") != 0:
    print "wrong dump"
    return
  
  holdit = time.time()
  
  start_data = dump.find("#")
  coords = dump[10:start_data]
  tail = dump[start_data+1:]
  width = int(coords[:coords.find("x")])
  height = int(coords[coords.find("x")+1:])
    
  # Make decode bit-stream
  stream = "" 
 
  while len(tail) > 1:
    
    end = tail.find("b")
    i = int(tail[:end])
    tail = tail[end+1:]
    while i > 0:
      stream += chr(0)
      i -= 1
  
    if len(tail) < 2: break;
  
    end = tail.find("f")
    i = int(tail[:end])
    tail = tail[end+1:]
    while i > 0:
      stream += chr(255)
      i -= 1
      
  im = Image.fromstring("L",(width,height), stream, "raw", "L")

  image_name = image_id +"_"+str(holdit)+".gif"
  im.save(settings.DATADIR+image_name,transparency=0);
  
  # Create associated measurement
  properties = dict(
    image = original_image,
    imagewidth = int(width),
    imageheight = int(height),
    path = image_name
  )  
  
  db_bitmap = Bitmap(**properties)
  db_bitmap.save()

  return image_name


#  brushStroke = self.cleaned_data['brushStroke']
#  fileName = self.cleaned_data['fileName']
#  #print self.cleaned_data['brushStroke']
#  #im = Image.open(fileName,"RGBA")
#  if os.path.exists(fileName):
#    im = Image.open(fileName)
#    im = im.convert("RGBA")
#  else:
#    im = Image.new("RGBA",(900,300))
#  draw = ImageDraw.Draw(im)
#
#  positions = brushStroke['positions']
#  #print brushStroke
#  #DRAWING CODE HERE
#    
#  previousPosition = 0
#  positionList = []
#  for position in positions:
#    positionList.append(position[0])
#    positionList.append(position[1])
#      
#  draw.line(positionList,fill=(255,0,0,100),width=3)
#  #print positionList
#    
#    
#  #print brushStroke.positions;
#    
#  del draw
#  im.save(fileName,transparency=0)
#  
#  #wrapper = FileWrapper(file(fileName))
#  #response = http.HttpResponse(wrapper, content_type='image/gif')
#  #response['Content-Length'] = os.path.getsize(fileName)