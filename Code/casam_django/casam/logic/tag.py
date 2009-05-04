from casam.models import Tag


def handle_add_tag(project, name):
  tag = Tag(name=name)
  tag.save()

  project.tags.add(tag)
  project.save()

def handle_select_tags(project, tags):
  project.tags = tags
  project.save()
