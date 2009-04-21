from casam.models import Project
from casam.models import MogelijkeMeting


def handle_add_project(name, mmeting1, mmeting2):
  project = Project(name=name)
  project.save()
  mm1 = MogelijkeMeting(name=mmeting1, project=project)
  mm1.save()
  mm2 = MogelijkeMeting(name=mmeting2, project=project)
  mm2.save()
