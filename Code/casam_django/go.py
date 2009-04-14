#!/usr/bin/env python
import os
import sys

def main():
  HERE = os.path.abspath(__file__)
  HERE = os.path.join(os.path.dirname(HERE), '..')
  HERE = os.path.normpath(HERE)

  DJANGO = [os.path.join(HERE, 'django')]

  sys.path = DJANGO + sys.path

  if len(sys.argv) == 1:
    sys.argv += ['runserver']

  import manage
  manage.main()

if __name__ == '__main__':
  main()

