from django.conf import settings
from django import http
from django.template import loader
from casam.views import handler
from casam.logic import pdm

class PDMTestView(handler.Handler):
  """Handler to test some PDM-related stuff
  """

  def get(self):
    context = self.getContext()
    
    pdmodel = pdm.tempPDM()
    pdm.analyse(pdmodel, '8dd68ac0-4a8f-11de-8f63-001f29478659', (1037,691))

    content = loader.render_to_string('pdm/main.html', dictionary=context)
    return http.HttpResponse(content)