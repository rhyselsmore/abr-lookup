import os

DEBUG = False
ABR_GUID = os.environ.get('ABR_GUID','None')

USERNAME = 'blah'
TOKEN = 'blah'

try:
    from settings_local import *
except:
    pass
