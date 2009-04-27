from casam.models import Annotation
from casam.models import Project


def handle_add_annotation(name, url, project_id):
  project = Project.objects.get(id=project_id);
  atn = Annotation(name=name, url=url, project=project)
  atn.save()
