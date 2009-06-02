from PIL import Image
from django.conf import settings
from casam.models import Bitmap
import time


def handle_bitmap_stream(dump,image_id,original_image,previous_id,r,g,b,mm):
  
  if not (r >= 0 and r <= 255 and 
          g >= 0 and g <= 255 and 
          b >= 0 and b <= 255):
    r = 255
    g = 0
    b = 0
  
  dump = dump.split("#")
  header = dump[0].split("x")
  body = dump[1]
  
  if header[0] != "_scanline:":
    print "wrong dump"
    return

  total_width  = int(header[1])
  total_height = int(header[2])
  min_x = int(header[3])
  max_x = int(header[4])
  min_y = int(header[5])
  max_y = int(header[6])
  
  block_width  = max_x - min_x + 1
  block_height = max_y - min_y + 1
  
  skip_before = min_y * total_width + min_x
  skip_between = min_x + (total_width - 1 - max_x)
  skip_after = (total_height - 1 - max_y) * total_width + (total_width - 1 - max_x)
  
  back_before  = ''.zfill(skip_before).replace('0',chr(0))
  back_after   = ''.zfill(skip_after).replace('0',chr(0))
  
  line_fill = 0

  # Make decode bit-stream
  stream = back_before 
 
  while len(body) > 1:
    
    # Find number of black pixels
    end = body.find("b")
    i = int(body[:end])
    body = body[end+1:]
    
    # Do we need to add lines?
    line_fill += i
    
    while line_fill > block_width:
      i += skip_between
      line_fill -= block_width
    
    # Write to the bit-stream
    stream += ''.zfill(i).replace('0',chr(0))
      
    if len(body) < 2: break;
  
    # Now do the foreground
    end = body.find("f")
    i = int(body[:end])
    body = body[end+1:]
    
    # Do we need to add lines?
    line_fill += i
    
    if line_fill > block_width:
      print "this should never happen:"
    
    # Write to the bit-stream
    stream += ''.zfill(i).replace('0',chr(255))

  stream += back_after

  # Build image
  im = Image.fromstring("L",(total_width,total_height), stream, "raw", "L")
  
  # Attach palette
  im.convert("P")
  palette = []
  for i in range(256):
    palette.extend((0, 0, 0))

  palette[765] = r  
  palette[766] = g
  palette[767] = b

  assert len(palette) == 768
  
  im.putpalette(palette)

  # Make database insert
  if previous_id == '0':    
    # Create associated measurement
    properties = dict(
      image = original_image,
      mogelijkemeting = mm,
      imagewidth = int(total_width),
      imageheight = int(total_height),
      minx = min_x,
      maxx = max_x,
      miny = min_y,
      maxy = max_y,
      project = original_image.project,
      name = "bitmap",
    )

    db_bitmap = Bitmap(**properties)
    db_bitmap.save()
    
    img_path = os.path.join(settings.DATADIR, db_bitmap.id)
    im.save(img_path,transparency=0);
    
    return db_bitmap.pk
  
  # Just overwrite previous image-file
  else:

    previous_image = Bitmap.objects.all().get(id=previous_id)
    previous_image.minx = min_x
    previous_image.maxx = max_x
    previous_image.miny = min_y
    previous_image.maxy = max_y
    previous_image.save()
    
    image_path = os.path.join(settings.DATADIR, previous_image.id)
    im.save(image_path,transparency=0);
    
    return previous_id