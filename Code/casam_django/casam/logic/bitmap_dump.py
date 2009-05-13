from PIL import Image

def handle_bitmap_stream(dump):
  
  if dump.find("_scanline:") != 0:
    print "wrong dump"
    return
  
  
  
  start_data = dump.find("#")
  coords = dump[10:start_data]
  tail = dump[start_data+1:]
  width = int(coords[:coords.find("x")])
  height = int(coords[coords.find("x")+1:])
  
  print dump
  
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
      
  print stream


  im = Image.fromstring("L",(width,height), stream, "raw", "L")

  print "hold it"
  
  im.save("test.bmp");

  print "image has been saved!"

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