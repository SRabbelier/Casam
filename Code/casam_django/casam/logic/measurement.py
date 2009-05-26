from casam.models import Measurement
from casam.models import PotentialMeasurement
from casam.models import Project


def getMeasurementsForProject(request, project_id):
  """
  """

  project = Project.objects.get(id=project_id)

  pots = PotentialMeasurement.objects.all().filter(project=project)

  result = {}

  for pot in pots:
    mess = Measurement.objects.select_related().filter(mogelijkemeting=pot)    
    result[pot] = dict((i.image, i) for i in mess)
    
  print result


def checkSanity(measurements):
  """
  """
  
  amount = min(measurements.values())
    