from casam.models import PotentialMeasurement


def handle_add_potential_measurement(project, name):
  if PotentialMeasurement.objects.all().filter(project=project).filter(name=name).count() == 0:
    pm = PotentialMeasurement(name=name, project=project)
    pm.save()
    return pm
  else:
    return None