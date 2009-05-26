from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from casam.logic import point_distribution_model as pdm
from casam.logic import pdmoverlay
from casam.logic import measurement
from casam.models import Project
from casam.models import PDM
from casam.models import Measurement
from casam.models import PotentialMeasurement

class PDMTestView(handler.Handler):
  """Handler to test some PDM-related stuff
  """

  def get(self):
    context = self.getContext()

    #Create a PDM and add it to database linked to first project
    pdmodel = pdm.makePDM()

    #for now get the firstproject
    firstProject = Project.objects.all()[0] 
    
    potentials = PotentialMeasurement.objects.all().filter(project=firstProject)
    
    pointsets = [] 
    measurementcount = len(Measurement.objects.select_related().filter(mogelijkemeting=potentials[1]))
    for measure in range(measurementcount):
      coords = []
      for pot in potentials:
        measurements = Measurement.objects.select_related().filter(mogelijkemeting=pot)
        print measurements[measure].x, measurements[measure].y
        coords.append((float(measurements[measure].x),float(measurements[measure].y),0.0)) 
      pdmodel.addPointSet(coords)     
      
    pdmodel.procrustes()
    pdmodel.pca()
    pdmodel.variations()    
    
    DATADIR = settings.DATADIR
    pdmObject = PDM(project=firstProject)
    pdmObject.save()
    imagePath = DATADIR + pdmObject.id + ".png"
    
    
    
    #Get the 

    #Create the overlay and save it
    pdmo = pdmoverlay.PDMOverlay((3456,2304))
    pdmo.drawMeans(pdmodel.meanPositions)
    pdmo.drawVariations(pdmodel.variationPositions)
    pdmo.saveImage(imagePath)
    
    content = loader.render_to_string('pdm/main.html', dictionary=context)
    return http.HttpResponse(content)
