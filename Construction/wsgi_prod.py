import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'Construction.settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
