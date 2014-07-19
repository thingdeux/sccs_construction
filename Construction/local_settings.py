from os import uname, path
import json

ENVIRONMENT_NAME = uname()[1]
PROJECT_ROOT = path.dirname(path.abspath(__file__))

if "webfaction" in ENVIRONMENT_NAME:
    DEBUG = False    
else:
    DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "031c6a21-f994-4331-aff8-f2aea039a53bdf9589a4-bf83-42b7-847a-6cbad53830541be2c746-ce98-48ba-8625-f76fa4d760f6"
NEVERCACHE_KEY = "5f5dd602-9221-4915-bd79-a547df0b017faade282c-28c0-406b-a0c1-68e57fcc611ab57091d8-51ce-481d-bff3-b7c8bee25493"

try:
    cred_file = open(path.join(PROJECT_ROOT, "cred.json") )
    cred = json.load(cred_file)    
except Exception as err:
    print ("Unable to open credential file - " + str(err))

if DEBUG:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_URL = '/static/'
    EMAIL_USE_TLS = True
    EMAIL_HOST = cred['EMAIL-DEBUG']['HOST']
    EMAIL_HOST_USER = cred['EMAIL-DEBUG']['USERNAME']
    EMAIL_HOST_PASSWORD = cred['EMAIL-DEBUG']['PASSWORD']
    EMAIL_PORT = cred['EMAIL-DEBUG']['PORT']
    #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    #Outputs E-Mail to the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

else:
    STATIC_URL = "http://jfff/static/"
    STATIC_ROOT = "/home/thingdeux/webapps/sccsstatic/"