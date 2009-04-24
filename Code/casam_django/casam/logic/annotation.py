from casam.models import Annotation


def handle_add_annotation(name, url):
  atn = Annotation(name=name, url=url)
  atn.save()
