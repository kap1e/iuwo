import sys

import os

INTERP = os.path.expanduser("/var/www/u2929175/data/iuwo/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app import application