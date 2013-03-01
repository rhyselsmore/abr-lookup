import os

DEBUG = False
ABR_GUID = os.environ.get('ABR_GUID','None')

try:
  from settings_local import *
except:
  pass
