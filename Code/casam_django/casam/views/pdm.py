from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from casam.logic import point_distribution_model as pdm
from casam.logic import pdmoverlay
from casam.models import Project
from casam.models import PDM


class PDMTestView(handler.Handler):
  """Handler to test some PDM-related stuff
  """

  def get(self):
    context = self.getContext()
    pdmodel = pdm.makePDM()

    firstProject = Project.objects.all()[0]
    
    DATADIR = settings.DATADIR
    pdmObject = PDM(project=firstProject)
    pdmObject.save()
    imagePath = DATADIR + pdmObject.id + ".png"

    
    pdmo = pdmoverlay.PDMOverlay((640,480))
    pdmo.drawMeans(pdmodel.meanPositions)
    pdmo.drawVariations(pdmodel.variationPositions)
    pdmo.saveImage(imagePath)
    
    content = loader.render_to_string('pdm/main.html', dictionary=context)
    return http.HttpResponse(content)
