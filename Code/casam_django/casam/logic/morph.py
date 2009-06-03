import vtk

from casam.logic import pdm
from casam.models import OriginalImage
from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import Project
from casam.models import PDM
from django.conf import settings
# read in coordinates

def createMorph(selectedImages,selectedPMs):
  '''
  Morph
  '''
  
  #get the measurements for the first image (our targets)
  mainImage = OriginalImage.objects.all().get(id=selectedImages[0])
   
  #now get the associated measurements
  measures = Measurement.objects.all().filter(id__in=selectedPMs[0])
  print 'measures', measures
  measures = [j for j in measures]
  measures.sort(key=lambda x: x.mogelijkemeting.name)
   
  coordsx = []
  coordsy = []
  for k, measurement in enumerate(measures):#for every measurement in the measurements
    coordsx.append(float(measurement.x))
    coordsy.append(float(measurement.y))
  
  print 'coordsx: ',coordsx  
  print 'coordsy: ',coordsy 
  
  r1 = vtk.vtkJPEGReader()
  r1.SetFileName(settings.DATADIR + mainImage.id + ".jpg")
  r1.Update() 
     
  # flip y coord (VTK has opposite convention), create 3-d coords
  ydim = r1.GetOutput().GetDimensions()[1]
  coords = [(x, ydim - y, 0) for (x,y) in zip(coordsx, coordsy)]
  
  print 'coords: ',coords
  
  # convert everything to vtkPoints
#  coords = [l2_255_coords, l5_coords]
#  lms = [vtk.vtkPoints() for _ in range(2)]
  
#  for idx, c in enumerate(coords):
#      lms[idx].SetNumberOfPoints(len(c))
#      for ptidx, pt in enumerate(c):
#          lms[idx].SetPoint(ptidx, pt)



#  #procrustes alignment
#  pdmodel,result = pdm.createPDM(selectedImages,selectedPMs)
#  if (result == 1):
#    pdmodel.procrustes()
#    pdmodel.pca()
#    #transformation = pdmodel.filterGPA.GetLandmarkTransform()
#    
#    transformation = vtk.vtkLandmarkTransform()
#    transformation.SetSourceLandmarks()
#    transformation.SetTargetLandmarks(pdmodel.getOutput(0))
#    transformation.SetModeToRigidBody()
#    
#    print transformation.GetSourceLandmarks()
#    print transformation.GetTargetLandmarks()
#    
#    transformation.Inverse()
#    transformation.Update()
#    
#    totalImages = []
#    for i in range(len(selectedImages)):
#      totalImages.append(OriginalImage.objects.all().get(id=selectedImages[i]))
#    
#    r1 = vtk.vtkJPEGReader()
#    r1.SetFileName(settings.DATADIR + totalImages[0].id + ".jpg")
#    r1.Update()  
#    # then transform
#    
#    
#    ir = vtk.vtkImageReslice()
#    
#    # use cubic for highest quality (slower)
#    # we're using linear here to shave off a few microseconds. :)
#    ir.SetInterpolationModeToLinear()
#    print "transform", transformation
#    ir.SetResliceTransform(transformation)
#    ir.SetInput(r1.GetOutput())
#    dw = vtk.vtkPNGWriter()
#    dw.SetFileName('c:\warp2.png')
#    dw.SetInput(ir.GetOutput())
#    dw.Write()
#  else:
#    return 0
#  #now transform the required image to the aligned image
#
#  potentialids = []
#  totalcoordsx = []
#  totalcoordsy = []
#  #coordinates aan de hand selected measurements goed opbouwen in vtkpoints
#  for i in range(len(selectedPMs)):#for the number of images
#    measures = Measurement.objects.all().filter(id__in=selectedPMs[i])#get the measurements
#    measures = [j for j in measures]
#    measures.sort(key=lambda x: x.mogelijkemeting.name)
#    
#    coordsx = []
#    coordsy = []
#    for k, measurement in enumerate(measures):#for every measurement in the measurements
#      if i == 0: #to check if the measurements come from the same potentialmeasurements
#        potentialids.append(measurement.mogelijkemeting.id)#on first run, store
#      elif potentialids[k] != measurement.mogelijkemeting.id:#on second run compare
#        return pdmodel, 0
#      coordsx.append(float(measurement.x))
#      coordsy.append(float(measurement.y))
#      
#    totalcoordsx.append(coordsx)
#    totalcoordsy.append(coordsy)
#  
#  totalImages = []
#  for i in range(len(selectedImages)):
#    totalImages.append(OriginalImage.objects.all().get(id=selectedImages[i]))
#    
#  totalcoords = []
#  first = True
#      
#  while len(totalImages) != 1:  
#    r1 = vtk.vtkJPEGReader()
#    r1.SetFileName(settings.DATADIR + totalImages[0].id + ".jpg")
#    r1.Update()  
#    
#    ydim1 = r1.GetOutput().GetDimensions()[1]
#    totalcoords.append([(x, ydim1 - y, 0) for (x,y) in zip(totalcoordsx[0], totalcoordsy[0])])
#
#    r2 = vtk.vtkJPEGReader()
#    r2.SetFileName(settings.DATADIR + totalImages[1].id + ".jpg")
#    r2.Update()
#    ydim2 = r2.GetOutput().GetDimensions()[1]
#    totalcoords.append([(x, ydim2 - y, 0) for (x,y) in zip(totalcoordsx[1], totalcoordsy[1])])
#  
#    # convert everything to vtkPoints
#    coords = [totalcoords[0], totalcoords[1]]
#    lms = [vtk.vtkPoints() for _ in range(2)]
#    
#    for idx, c in enumerate(coords):
#        lms[idx].SetNumberOfPoints(len(c))
#        for ptidx, pt in enumerate(c):
#            lms[idx].SetPoint(ptidx, pt)
#    
#    # setup the transform
#    tps = vtk.vtkThinPlateSplineTransform()
#    tps.SetBasisToR2LogR()
#    tps.SetSourceLandmarks(lms[0])
#    lms[0].Modified()
#    tps.SetTargetLandmarks(lms[1])
#    lms[1].Modified()
#    # the tps transforms from lms[0] to lms[1] (see the docs)
#    # but we're going to apply this as a reslice transform, which means
#    # the grid and not the coordinates is transformed, which means we need
#    # the inverse.  This is slow.
#    tps.Inverse()
#    tps.Update()
#   
#    # then transform
#    ir = vtk.vtkImageReslice()
#    
#    # use cubic for highest quality (slower)
#    # we're using linear here to shave off a few microseconds. :)
#    ir.SetInterpolationModeToLinear()
#    ir.SetResliceTransform(tps)
#    ir.SetInput(r1.GetOutput())
#    ir.SetInformationInput(r2.GetOutput())
#        
#    totalImages.pop(0)
#    totalImages.pop(0)
#    
#    totalImages.insert(0, ir)
#    first = False
#  
#  dw = vtk.vtkPNGWriter()
#  dw.SetFileName('c:\warp.png')
#  dw.SetInput(totalImages[0].GetOutput())
#  dw.Write()
#  
#
#  return True, 1
#  #images readen aan de hand selectedImages
  
