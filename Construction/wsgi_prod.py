import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'carlos.settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
