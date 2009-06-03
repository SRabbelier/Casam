import vtk

from casam.logic import point_distribution_model as pdm
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
  
  #procrustes alignment
  pdmodel = pdm.makePDM()
  
  potentialids = []
  totalcoordsx = []
  totalcoordsy = []
  #coordinates aan de hand selected measurements goed opbouwen in vtkpoints
  for i in range(len(selectedPMs)):#for the number of images
    measures = Measurement.objects.all().filter(id__in=selectedPMs[i])#get the measurements
    coordsx = []
    coordsy = []
    
    for k in range(len(measures)):#for every measurement in the measurements
      measurement = measures[k]
      if i == 0: #to check if the measurements come from the same potentialmeasurements
        potentialids.append(measurement.mogelijkemeting.id)#on first run, store
      elif potentialids[k] != measurement.mogelijkemeting.id:#on second run compare
        return pdmodel, 0
      coordsx.append(float(measurement.x))
      coordsy.append(float(measurement.y))
      
    totalcoordsx.append(coordsx)
    totalcoordsy.append(coordsy)
  
  totalImages = []
  for i in range(len(selectedImages)):
    totalImages.append(OriginalImage.objects.all().get(id=selectedImages[i]))
  
  totalcoords = []
  first = True
  while len(totalImages) != 1:
    if first:
      r1 = vtk.vtkJPEGReader()
      r1.SetFileName(DATADIR + totalImages[0].path)
      r1.Update()
    else:
      r1 = totalImages[0]
    
    
    ydim1 = r1.GetOutput().GetDimensions()[1]
    totalcoords[0] = [(x, ydim1 - y, 0) for (x,y) in zip(totalcoordsx[0], totalcoordsy[0])]
    
    r2 = vtk.vtkJPEGReader()
    r2.SetFileName(DATADIR + totalImages[1].path)
    r2.Update()
    ydim2 = r2.GetOutput().GetDimensions()[1]
    totalcoords[1] = [(x, ydim2 - y, 0) for (x,y) in zip(totalcoordsx[1], totalcoordsy[1])]
    
    # convert everything to vtkPoints
    coords = [totalcoords[0], totalcoords[1]]
    lms = [vtk.vtkPoints() for _ in range(2)]
    
    for idx, c in enumerate(coords):
        lms[idx].SetNumberOfPoints(len(c))
        for ptidx, pt in enumerate(c):
            lms[idx].SetPoint(ptidx, pt)
    
    # setup the transform
    tps = vtk.vtkThinPlateSplineTransform()
    tps.SetBasisToR2LogR()
    tps.SetSourceLandmarks(lms[0])
    lms[0].Modified()
    tps.SetTargetLandmarks(lms[1])
    lms[1].Modified()
    # the tps transforms from lms[0] to lms[1] (see the docs)
    # but we're going to apply this as a reslice transform, which means
    # the grid and not the coordinates is transformed, which means we need
    # the inverse.  This is slow.
    tps.Inverse()
    tps.Update()
    
    # then transform
    ir = vtk.vtkImageReslice()
    # use cubic for highest quality (slower)
    # we're using linear here to shave off a few microseconds. :)
    ir.SetInterpolationModeToLinear()
    ir.SetResliceTransform(tps)
    ir.SetInput(r1.GetOutput())
    ir.SetInformationInput(r2.GetOutput())
        
    totalImages.pop(0)
    totalImages.pop(0)
    
    totalImages.insert(0, ir)
    first = False
    
  return True, 1
  #images readen aan de hand selectedImages
  
