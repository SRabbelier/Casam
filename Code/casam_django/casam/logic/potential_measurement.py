from casam.models import PotentialMeasurement
from casam.models import PotentialMeasurementType


def handle_add_potential_measurement(project, type, name):
  if PotentialMeasurement.objects.all().filter(project=project).filter(type=type).filter(name=name).count() == 0:
    pm = PotentialMeasurement(name=name, type=type, project=project)
    pm.save()
    return pm
  else:
    return None
  
def handle_add_potential_measurement_type(project, name):
  if PotentialMeasurementType.objects.all().filter(project=project).filter(name=name).count() == 0:
    pmt = PotentialMeasurementType(name=name, project=project)
    pmt.save()
    return pmt
  else:
    return None