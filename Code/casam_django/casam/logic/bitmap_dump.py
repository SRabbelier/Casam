def handle_bitmap_stream():
  brushStroke = self.cleaned_data['brushStroke']
  fileName = self.cleaned_data['fileName']
  #print self.cleaned_data['brushStroke']
  #im = Image.open(fileName,"RGBA")
  if os.path.exists(fileName):
    im = Image.open(fileName)
    im = im.convert("RGBA")
  else:
    im = Image.new("RGBA",(900,300))
  draw = ImageDraw.Draw(im)

  positions = brushStroke['positions']
  #print brushStroke
  #DRAWING CODE HERE
    
  previousPosition = 0
  positionList = []
  for position in positions:
    positionList.append(position[0])
    positionList.append(position[1])
      
  draw.line(positionList,fill=(255,0,0,100),width=3)
  #print positionList
    
    
  #print brushStroke.positions;
    
  del draw
  im.save(fileName,transparency=0)
  
  #wrapper = FileWrapper(file(fileName))
  #response = http.HttpResponse(wrapper, content_type='image/gif')
  #response['Content-Length'] = os.path.getsize(fileName)