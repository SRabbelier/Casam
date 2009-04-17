import os
import sys

HERE = os.path.abspath(__file__)
HERE = os.path.join(os.path.dirname(HERE), '..')
HERE = os.path.normpath(HERE)

sys.path = [HERE] + sys.path
