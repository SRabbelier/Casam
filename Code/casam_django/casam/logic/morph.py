import vtk

from casam.logic import pdm
from casam.models import OriginalImage
from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import Project
from casam.models import PDM
from casam.models import Bitmap
from django.conf import settings

from PIL import Image
# read in coordinates

def createMorph(selectedImages,selectedPMs):
  '''
  Morph
  '''
  
  #get the measurements for the first image (our targets)
  mainImage = OriginalImage.objects.all().get(id=selectedImages[0])
  potentialids = [] 
  #now get the associated measurements
  measures = Measurement.objects.all().filter(id__in=selectedPMs[0])
  measures = [j for j in measures]
  measures.sort(key=lambda x: x.mogelijkemeting.name)
   
  coordsx = []
  coordsy = []
  for k, measurement in enumerate(measures):#for every measurement in the measurements
    coordsx.append(float(measurement.x))
    coordsy.append(float(measurement.y))
    potentialids.append(measurement.mogelijkemeting.id)
  r1 = vtk.vtkJPEGReader()
  r1.SetFileName(settings.DATADIR + mainImage.id + ".jpg")
  r1.Update() 

  # flip y coord (VTK has opposite convention), create 3-d coords
  ydim = r1.GetOutput().GetDimensions()[1]
  coords = [(x, ydim - y, 0) for (x,y) in zip(coordsx, coordsy)]
  
  # convert everything to vtkPoints
  lmt = vtk.vtkPoints()
  lmt.SetNumberOfPoints(len(coords))
  for i, coord in enumerate(coords):
    lmt.SetPoint(i,coord)
  
  #The target is set, let's get the sources
  images = []
  selectedImages.pop(0)
  selectedPMs.pop(0)
  for id in selectedImages:
    images.append(OriginalImage.objects.all().get(id=id))
  #images = list(OriginalImage.objects.all().filter(id__in=selectedImages))

  transformations = []
  morphtransformations = []
  
  img = OriginalImage(project=mainImage.project, name='warpedimage')
  img.save()
  imp = Image.open(settings.DATADIR + mainImage.id + '.jpg')
  imp.save(settings.DATADIR + img.id + '.jpg', 'JPEG')  
  orig_bitmaps = Bitmap.objects.all().filter(image=mainImage)
  
  print "original bitmaps: ", orig_bitmaps
  for bm in orig_bitmaps:
    #store bitmaps of mainImage as sub of img
    bitmap = Bitmap(project=img.project, name='warpedbitmap', image=img, 
                      mogelijkemeting=bm.mogelijkemeting, imagewidth=bm.imagewidth, 
                      imageheight=bm.imageheight, minx=bm.minx, miny=bm.miny, maxx=bm.maxx, maxy=bm.maxy)
    bitmap.save()
      
    bitmap_image = Image.open(settings.DATADIR + bm.id + '.gif')
    bitmap_image = bitmap_image.convert("RGBA")
    bitmap_image.save(settings.DATADIR + bitmap.id + '.gif', transparency=0)
    

  for i in range(len(images)):#for each image
    measures = Measurement.objects.all().filter(id__in=selectedPMs[i])#get measurements
    measures = [j for j in measures]
    measures.sort(key=lambda x: x.mogelijkemeting.name)
    coordsx = []
    coordsy = []    
    for k, measurement in enumerate(measures):#for every measurement in the measurements
      coordsx.append(float(measurement.x))
      coordsy.append(float(measurement.y))
      if potentialids[k] != measurement.mogelijkemeting.id:#on second run compare
        return img, 0
    r = vtk.vtkJPEGReader()
    r.SetFileName(settings.DATADIR + images[i].id + ".jpg")
    r.Update()

    ydim = r.GetOutput().GetDimensions()[1]
    coordso = [(x, ydim - y, 0) for (x,y) in zip(coordsx, coordsy)]
    lms = vtk.vtkPoints()
    lms.SetNumberOfPoints(len(coordso))
    for k, coord in enumerate(coordso):
      lms.SetPoint(k,coord)

    transformation = vtk.vtkLandmarkTransform()
    transformation.SetTargetLandmarks(lmt)  
    lmt.Modified()
    transformation.SetSourceLandmarks(lms)
    lms.Modified()
    transformation.SetModeToRigidBody()
    transformation.Inverse()
    transformation.Update()
    out = vtk.vtkPoints()
    transformation.TransformPoints(lms,out)
    transformations.append(transformation)
    # then transform
    ir = vtk.vtkImageReslice()
    # use cubic for highest quality (slower)
    # we're using linear here to shave off a few microseconds. :)
    ir.SetInterpolationModeToNearestNeighbor()
    #ir.SetInterpolationModeToLinear()
    ir.SetResliceTransform(transformation)
    ir.SetInput(r.GetOutput())
    ir.SetInformationInput(r1.GetOutput())
    w = vtk.vtkJPEGWriter()
    w.SetFileName('translated'+images[i].id+'.jpg')
    w.SetInput(ir.GetOutput())
    w.Write()
    r2 = vtk.vtkJPEGReader()
    r2.SetFileName('translated'+images[i].id+'.jpg')
    r2.Update()  
 

    
    morphtransform = vtk.vtkThinPlateSplineTransform()
    
    morphtransform.SetBasisToR2LogR()
    morphtransform.SetSourceLandmarks(out)
    out.Modified()
    morphtransform.SetTargetLandmarks(lmt)
    lmt.Modified()
    #morphtransform.SetModeToRigidBody()
    morphtransform.Inverse()
    morphtransform.Update()
    morphtransformations.append(morphtransform)
    ir.SetResliceTransform(morphtransform)
    ir.SetInput(r2.GetOutput())
    ir.SetInformationInput(r1.GetOutput())
#    w2 = vtk.vtkJPEGWriter()
#    w2.SetFileName('morphed'+images[i].id+'.jpg')
#    w2.SetInput(ir.GetOutput())
#    w2.Write()
    
    
    bitmaps = Bitmap.objects.all().filter(image=images[i])
    
    print bitmaps
    
    for bm in bitmaps:
      location = settings.DATADIR + bm.id + ".gif"
      im = Image.open(location)
      im = im.convert("RGBA")
      im.save(settings.DATADIR + bm.id + ".png", "PNG")

      r3 = vtk.vtkPNGReader()
      r3.SetFileName(settings.DATADIR + bm.id + '.png')
      r3.Update()
      
      print bm  
      ir.SetInput(r3.GetOutput())
      ir.SetInformationInput(r1.GetOutput())
      
      w3 = vtk.vtkPNGWriter()
      w3.SetFileName('morphinatingthepeasants'+bm.id+'.png')
      w3.SetInput(ir.GetOutput())
      w3.Write()
      
      #im2 = Image.open(settings.DATADIR + mainImage.id + '.jpg')
      #im2.save(settings.DATADIR + img.id + '.jpg', 'JPEG')
      
      bitmap = Bitmap(project=img.project, name='warpedbitmap', image=img, 
                      mogelijkemeting=bm.mogelijkemeting, imagewidth=bm.imagewidth, 
                      imageheight=bm.imageheight, minx=bm.minx, miny=bm.miny, maxx=bm.maxx, maxy=bm.maxy)
      bitmap.save()
      
      im = Image.open('morphinatingthepeasants'+bm.id+'.png')
      im = im.convert("RGBA")
      im.save(settings.DATADIR + bitmap.id + '.gif', transparency=0)
      

  return img, 1
#  #images readen aan de hand selectedImages
  
