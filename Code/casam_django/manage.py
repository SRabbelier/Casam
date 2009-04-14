#!/usr/bin/python

import os
import sys

from django.core.management import execute_manager

try:
  import settings # Assumed to be in the same directory.
except ImportError:
  import sys
  sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r." % __file__)
  sys.exit(1)

def main():
  HERE = os.path.abspath(__file__)
  HERE = os.path.join(os.path.dirname(HERE), '..')
  HERE = os.path.normpath(HERE)

  sys.path = [HERE] + sys.path

  execute_manager(settings)

if __name__ == "__main__":
  main()
