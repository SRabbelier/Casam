from PIL import Image
from django.conf import settings
from casam.models import Bitmap
import time
import os

def handle_bitmap_stream(dump,original_image,previous_id,r,g,b,mm):
  """ With the string representation of a bitmap; the original_image
     this bitmap is painted over; the id of the previous bitmap;
     the color information and the id of the possible measurement
     this function saves the dump as a .gif-file and puts it in the db.
  """ 

  # Check the header
  if dump == "_empty":
    print "Empty bitmap submitted"
    return previous_id

  # Initialise color information
  if not (r >= 0 and r <= 255 and 
          g >= 0 and g <= 255 and 
          b >= 0 and b <= 255):
    r = 255
    g = 0
    b = 0
    
  # Split dump in header and body
  dump = dump.split("#")
  header = dump[0].split("x")
  body = dump[1]

  # Check the header
  if header[0] != "_scanline:":
    print "wrong dump"
    return

  # Load needed variables from header
  total_width  = int(header[1])
  total_height = int(header[2])
  min_x = int(header[3])
  max_x = int(header[4])
  min_y = int(header[5])
  max_y = int(header[6])
  
  
  # Derive needed variables from loaded variables
  block_width  = max_x - min_x + 1
  block_height = max_y - min_y + 1


  skip_before = min_y * total_width + min_x
  skip_between = min_x + (total_width - 1 - max_x)
  skip_after = (total_height - 1 - max_y) * total_width + (total_width - 1 - max_x)
  
  # Create string to fill before and after block
  fill_before  = ''.zfill(skip_before).replace('0',chr(0))
  fill_after   = ''.zfill(skip_after).replace('0',chr(0))
  
  # Keep track of the amount of pixels that is currently on the line
  # in the block to be able to determine how often we need to add skip_between
  line_fill = 0
  
  # Make decode bit-stream
  stream = fill_before 
 
  # Do as long as there is still data in body
  while len(body) > 1:
    
    # Find number of black pixels
    end = body.find("b")
    i = int(body[:end])
    body = body[end+1:]
    
    # We need at least to add i pixels
    line_fill += i
    
    # Each whole amount block_with fits in line_fill,
    # we need to add skip_between
    
    while line_fill > block_width:
      
      i += skip_between
      line_fill -= block_width
      
    # Write i background pixels to the bit-stream
    stream += ''.zfill(i).replace('0',chr(0))

    # Stop if we now finished the end of the string data
    if len(body) < 2: break;
  
    # Now do the foreground
    end = body.find("f")
    i = int(body[:end])
    body = body[end+1:]
    
    # If we now need to add lines, it should
    # also be background outside the block
    if line_fill + i > block_width:
      
      # First write foreground pixels to fill the current row in the block
      stream += ''.zfill(block_width - line_fill).replace('0', chr(255))
      
      # We still have this much pixels to write
      line_fill = i - (block_width - line_fill)
      
      # As long as we can fill full block lines 
      while line_fill > block_width:

        # First write background line to get back to block
        stream += ''.zfill(skip_between).replace('0', chr(0))
        
        # Then write a full line foreground-data
        stream += ''.zfill(block_width).replace('0', chr(255))
        line_fill -= block_width

      # Return to a new line (by filling space outside the block)
      stream += ''.zfill(skip_between).replace('0', chr(0))

      # We still have a number of pixels left to write
      i = line_fill
    
    # Otherwise we also need to remember this set of pixels
    else:
      line_fill += i
 
    # Write to the bit-stream
    stream += ''.zfill(i).replace('0',chr(255))

  stream += fill_after
  
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

    
    img_path = os.path.join(settings.DATADIR, db_bitmap.id + ".gif")
    
    im.save(img_path,transparency=0)
    return db_bitmap.id
  
  # Just overwrite previous image-file
  else:
    previous_image = Bitmap.objects.all().get(id=previous_id)
    previous_image.minx = min_x
    previous_image.maxx = max_x
    previous_image.miny = min_y
    previous_image.maxy = max_y
    previous_image.save()
    
    image_path = os.path.join(settings.DATADIR, previous_image.id + '.gif')
    im.save(image_path,transparency=0);
    
    return previous_id