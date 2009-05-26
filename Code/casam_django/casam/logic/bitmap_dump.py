from PIL import Image
from django.conf import settings
from casam.models import Bitmap
import time


def handle_bitmap_stream(dump,image_id,original_image,previous_id,r,g,b):
  
  if dump.find("_scanline:") != 0:
    print "wrong dump"
    return
  
  if not (r >= 0 and r <= 255 and g >= 0 and g <= 255 and b >= 0 and b <= 255):
    r = 255
    g = 0
    b = 0
  
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
  im.convert("P")
  
  palette = []
  for i in range(256):
    palette.extend((0, 0, 0))

  palette[765] = r  
  palette[766] = g
  palette[767] = b

  assert len(palette) == 768
  
  im.putpalette(palette)

  
  if previous_id == '0':
  
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
    return db_bitmap.pk
  
  else:
    
    previous_image = Bitmap.objects.filter(id=previous_id).get()
    image_name = previous_image.path
    print settings.DATADIR+image_name
    im.save(settings.DATADIR+image_name,transparency=0);
    return previous_id


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