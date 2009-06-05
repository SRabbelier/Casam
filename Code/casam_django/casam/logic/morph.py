import vtk
import tempfile
import os

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
  """
  Translates and rotate the bitmaps based on the shapedefining landmarks (selectedPMs)
  of the associated image to the target image (first image).
  Morphs the result so that the bitmap overlay on the first image is valid for the first image.  
  """
  
  #save the temporary results here later:
  os_temp_path = tempfile.gettempdir()
  
  #get the measurements for the first image (our targets)
  mainImage = OriginalImage.objects.all().get(id=selectedImages[0])
  potentialids = [] 
  #now get the associated measurements
  measures = Measurement.objects.all().filter(id__in=selectedPMs[0]).filter(mogelijkemeting__shapedefining=True)
  measures = [j for j in measures]
  measures.sort(key=lambda x: x.mogelijkemeting.name)
   
  coordsx = []
  coordsy = []
  for k, measurement in enumerate(measures):
    coordsx.append(float(measurement.x))
    coordsy.append(float(measurement.y))
    potentialids.append(measurement.mogelijkemeting.id)
  r1 = vtk.vtkJPEGReader()
  r1.SetFileName(settings.DATADIR + mainImage.id + ".jpg")
  r1.Update() 

  # flip y coord (VTK has opposite convention), create 3-d coords (z=0)
  ydim = r1.GetOutput().GetDimensions()[1]
  coords = [(x, ydim - y, 0) for (x,y) in zip(coordsx, coordsy)]
  
  # convert everything to vtkPoints
  lmt = vtk.vtkPoints()
  lmt.SetNumberOfPoints(len(coords))
  for i, coord in enumerate(coords):
    lmt.SetPoint(i,coord)
  
  #The target is clear, let's get to work, get the source images...
  images = []
  #we don't need the first image or its measures anymore, because they don't need to be transformed or morphed
  selectedImages.pop(0)
  selectedPMs.pop(0)
  for id in selectedImages:
    images.append(OriginalImage.objects.all().get(id=id))

  transformations = []
  morphtransformations = []
  
  #Create a new database object for the target image to associate the bitmaps with
  img = OriginalImage(project=mainImage.project, name='MorphedImage')
  img.save()
  imp = Image.open(settings.DATADIR + mainImage.id + '.jpg')
  imp.save(settings.DATADIR + img.id + '.jpg', 'JPEG')  
  orig_bitmaps = Bitmap.objects.all().filter(image=mainImage)
  
  for bm in orig_bitmaps:
    #store bitmaps of mainImage as sub of img
    bitmap = Bitmap(project=img.project, name='warpedbitmap', image=img, 
                      mogelijkemeting=bm.mogelijkemeting, imagewidth=bm.imagewidth, 
                      imageheight=bm.imageheight, minx=bm.minx, miny=bm.miny, maxx=bm.maxx, maxy=bm.maxy)
    bitmap.save()
      
    bitmap_image = Image.open(settings.DATADIR + bm.id + '.gif')
    bitmap_image = bitmap_image.convert("RGBA")
    bitmap_image.save(settings.DATADIR + bitmap.id + '.gif', transparency=0)
    
  #now get the other images and perform our transformations
  for i in range(len(images)):
    measures = Measurement.objects.all().filter(id__in=selectedPMs[i]).filter(mogelijkemeting__shapedefining=True)#get measurements
    measures = [j for j in measures]
    measures.sort(key=lambda x: x.mogelijkemeting.name)
    coordsx = []
    coordsy = []    
    for k, measurement in enumerate(measures):
      coordsx.append(float(measurement.x))
      coordsy.append(float(measurement.y))
      if potentialids[k] != measurement.mogelijkemeting.id: #the potentialmeasurements do not match up to the ones in the target image
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
    #size matters, so set the mode to Rigid Body (also known as do not scale please)
    transformation.SetModeToRigidBody()
    transformation.Inverse()
    transformation.Update()
    out = vtk.vtkPoints()#this will be the source of our morph transform
    transformation.TransformPoints(lms,out)
    transformations.append(transformation)
    ir = vtk.vtkImageReslice()
    # we're not using linear, because we want to improve the quality of the bitmaps
    ir.SetInterpolationModeToNearestNeighbor()
    ir.SetResliceTransform(transformation)
    ir.SetInput(r.GetOutput())
    ir.SetInformationInput(r1.GetOutput())
    w = vtk.vtkJPEGWriter()
    w.SetFileName(os_temp_path+'translated'+images[i].id+'.jpg')
    w.SetInput(ir.GetOutput())
    w.Write()
    r2 = vtk.vtkJPEGReader()
    r2.SetFileName(os_temp_path+'translated'+images[i].id+'.jpg')
    r2.Update()  
 
    # the mighty morphing ThinPlateSplineTransform
    morphtransform = vtk.vtkThinPlateSplineTransform()
    morphtransform.SetBasisToR2LogR()
    morphtransform.SetSourceLandmarks(out)
    out.Modified()
    morphtransform.SetTargetLandmarks(lmt)
    lmt.Modified()
    morphtransform.Inverse()
    morphtransform.Update()
    morphtransformations.append(morphtransform)
    ir.SetResliceTransform(morphtransform)
    ir.SetInput(r2.GetOutput())
    ir.SetInformationInput(r1.GetOutput())
    
    bitmaps = Bitmap.objects.all().filter(image=images[i])
    
    #now perform the total transformation on all bitmaps
    for bm in bitmaps:
      location = settings.DATADIR + bm.id + ".gif"
      im = Image.open(location)
      im = im.convert("RGBA")
      im.save(settings.DATADIR + bm.id + ".png", "PNG")

      r3 = vtk.vtkPNGReader()
      r3.SetFileName(settings.DATADIR + bm.id + '.png')
      r3.Update()
      
      ir.SetInput(r3.GetOutput())
      ir.SetInformationInput(r1.GetOutput())
      
      w3 = vtk.vtkPNGWriter()
      w3.SetFileName(os_temp_path+'morphed'+bm.id+'.png')
      w3.SetInput(ir.GetOutput())
      w3.Write()
      
      bitmap = Bitmap(project=img.project, name='warpedbitmap', image=img, 
                      mogelijkemeting=bm.mogelijkemeting, imagewidth=bm.imagewidth, 
                      imageheight=bm.imageheight, minx=bm.minx, miny=bm.miny, maxx=bm.maxx, maxy=bm.maxy)
      bitmap.save()
      
      im = Image.open(os_temp_path+'morphed'+bm.id+'.png')
      im = im.convert("RGBA")
      im.save(settings.DATADIR + bitmap.id + '.gif', transparency=0)
      

  return img, 1