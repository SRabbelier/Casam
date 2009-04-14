#!/usr/bin/env python
import os
import sys

HERE = os.path.abspath(__file__)
HERE = os.path.join(os.path.dirname(HERE), '..')
HERE = os.path.normpath(HERE)

DJANGO = [os.path.join(HERE, 'django')]

sys.path = DJANGO + sys.path

sys.argv = sys.argv[:1]
sys.argv += ['runserver']

import manage
manage.main()
