from casam.models import Project
from casam.models import ProjectMeasurementList


def handle_add_project(profile, name, description):
  project = Project(name=name, description=description)
  project.save()
  profile.read.add(project)
  profile.write.add(project)
  profile.save()


def handle_remove_project(id):
  Project.objects.all().get(id=id).delete()
