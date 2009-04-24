from casam.models import Annotation


def handle_add_project(name, url):
  atn = Annotation(name=name, url=url)
  atn.save()
