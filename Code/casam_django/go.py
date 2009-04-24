#!/usr/bin/env python
import os
import sys

# Log errors.
def log_exception(*args, **kwds):
  """Function used for logging exceptions.
  """
  import logging
  logging.exception('Exception in request:')


def main():
  HERE = os.path.abspath(__file__)
  HERE = os.path.join(os.path.dirname(HERE), '..')
  HERE = os.path.normpath(HERE)

  WERKZEUG = [os.path.join(HERE, 'werkzeug')]
  DJANGO_EXTENSIONS = [os.path.join(HERE, 'django_extensions')]
  DJANGO = [os.path.join(HERE, 'django')]
  CASAM = [os.path.join(HERE, 'casam_django', 'casam')]
  PIL = [os.path.join(HERE, 'PIL')]

  sys.path = PIL + WERKZEUG + DJANGO_EXTENSIONS + DJANGO + CASAM + sys.path

  print sys.path
  if len(sys.argv) == 1:
    sys.argv += ['runserver_plus']

  import manage
  manage.main()

  from casam_django.casam.models import Project
  pr1 = Project(name='Project A')
  pr1.save()
  pr2 = Project(name='Project B')
  pr2.save()
  
  from django.contrib.auth.models import Group
  try:
    gr1 = Group.objects.get(name='Beheerder')
  except Group.DoesNotExist:
    gr1 = Group(name='Beheerder')
    gr1.save()
    gr2 = Group(name='Chirurg')
    gr2.save()
    gr3 = Group(name='Onderzoeker')
    gr3.save()

  from django.conf import settings
  settings.DEBUG = True

  import django.core.signals

  # Log all exceptions detected by Django.
  django.core.signals.got_request_exception.connect(log_exception)


if __name__ == '__main__':
  main()
