#!/usr/bin/env python
import os
import sys

from django.conf import settings

def main():
  HERE = os.path.abspath(__file__)
  HERE = os.path.join(os.path.dirname(HERE), '..')
  HERE = os.path.normpath(HERE)

  DJANGO = [os.path.join(HERE, 'django')]
  CASAM = [os.path.join(HERE, 'casam_django', 'casam')]
  #CASAM_CASAM = [os.path.join(CASAM, 'casam')]

  sys.path = DJANGO + CASAM + sys.path
  #sys.path = CASAM + sys.path
  #print sys.path
  #sys.path = CASAM_CASAM + sys.path
  
  #print sys.path

  if len(sys.argv) == 1:
    sys.argv += ['runserver']

  import manage
  manage.main()
  
  from casam_django.casam.models import Project
  pr1 = Project(name='Project A')
  pr1.save()
  pr2 = Project(name='Project B')
  pr2.save()

  settings.DEBUG = True

if __name__ == '__main__':
  main()

