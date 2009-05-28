from casam.models import OriginalImage
from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import Project
from casam.models import PDM
from casam.logic import pdmoverlay
from casam.logic import point_distribution_model as pdm
from django.conf import settings
from PIL import Image

def tempPDM():
  '''
  Temporary PDM Creation without providing project, selected possible measurements and selected images
  '''
  pdmodel = pdm.makePDM()
  project = Project.objects.all()[0] 
  potentials = PotentialMeasurement.objects.all().filter(project=project)

  totalmeasure = 0
  measurementcount = len(Measurement.objects.select_related().filter(mogelijkemeting=potentials[0]))
  for measure in range(measurementcount):
    coords = []
    for pot in potentials:
      measurements = Measurement.objects.select_related().filter(mogelijkemeting=pot)
      if totalmeasure == 0:
        totalmeasure = len(measurements)
        coords.append((float(measurements[measure].x),float(measurements[measure].y),0.0))
      elif totalmeasure == len(measurements): 
        coords.append((float(measurements[measure].x),float(measurements[measure].y),0.0))
      else:
        totalmeasure = 0
        break   
    if totalmeasure != 0:
      pdmodel.addPointSet(coords)
    else:
      #raise some kind of exception here somehow!
      pdmodel = pdm.makePDM()
      pdmodel.addPointSet([(100,100,0)])
      pdmodel.addPointSet([(250,150,0)])
      break
  return pdmodel

def createPDM(selectedImages,selectedPMs):
  '''
  Create the Point Distribution Model from the selected measurements
  '''
  pdmodel = pdm.makePDM()
  for i in range(len(selectedPMs)):
    measures = Measurement.objects.all().filter(id__in=selectedPMs[i])
    coords = []
    for k in range(len(measures)):
      measurement = measures[k]
      coords.append((float(measurement.x),float(measurement.y),0.0))
    pdmodel.addPointSet(coords)
  return pdmodel
      
def analyse(pdmodel, projectid, selectedImages):
  '''
  Analyse the given pdmodel using Procrustes & PCA, save to database and to image
  '''
  pdmodel.procrustes()
  pdmodel.pca()
  pdmodel.variations()
  pdmObject = PDM(project = Project.objects.all().get(id=projectid))
  pdmObject.save()
  
  DATADIR = settings.DATADIR
  
  #get size from the first original image (all images should be same size for analysis to work properly anyway
  image = OriginalImage.objects.all().get(id=selectedImages[0])
  im = Image.open(DATADIR+image.path)
  pdmo = pdmoverlay.PDMOverlay(im.size)
  pdmo.drawVariations(pdmodel.variationPositions)
  pdmo.drawMeans(pdmodel.meanPositions)
  
  imagePath = DATADIR + pdmObject.id + ".png"
  pdmo.saveImage(imagePath)

    