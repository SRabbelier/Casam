from casam.models import PotentialMeasurement


def handle_add_potential_measurement(project, name):
  pm = PotentialMeasurement(name=name, project=project)
  pm.save()
