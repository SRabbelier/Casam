from casam.models import Project
from casam.models import State


def handle_add_project(profile, name, description):
  project = Project(name=name, description=description)
  project.save()
  profile.read.add(project)
  profile.write.add(project)
  profile.save()
  return project

def handle_remove_project(id):
  Project.objects.all().get(id=id).delete()

def handle_add_state(profile, name, serializedState,projectID):
  #print projectID
  stateProject = Project.objects.all().get(id=projectID)
  state = State(name=name, serializedState=serializedState,project = stateProject)
  state.save()