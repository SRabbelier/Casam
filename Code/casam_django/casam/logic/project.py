import os
import zipfile
import datetime

from django.conf import settings

from casam.models import Project
from casam.models import State

def run():
  return "Uploaded export does not define a run method."


def handle_import_project(file, profile):
  zip = zipfile.ZipFile(file, mode='r')
  files = zip.namelist()
  exportables = [i for i in files if i != 'export_script.py']
  for i in exportables:
    filename = os.path.join(settings.DATADIR, i)
    print filename
    f = open(filename, 'wb')
    f.write(zip.read(i))
    f.close()
  
  script = zip.read('export_script.py')
  script = script.replace('\r\n','\n')
  compiled = compile(script, 'compile_result.txt', 'exec')
  print compiled
  exec(compiled)
  result = run(profile)
  print result


def handle_add_project(profile, name, description):
  project = Project(name=name, description=description)
  project.save()
  profile.read.add(project)
  profile.write.add(project)
  profile.save()
  return project

def handle_remove_project(id):
  Project.objects.all().get(id=id).delete()

def handle_add_state(profile, name, serializedState,projectID,width,height):
  #print projectID
  stateProject = Project.objects.all().get(id=projectID)
  state = State(name=name, serializedState=serializedState,project = stateProject, width=width, height=height)
  state.save()