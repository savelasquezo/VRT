from .settings  import *

DEBUG = False

ALLOWED_HOSTS = ["167.71.28.44","vrtfund.com","www.vrtfund.com"]

CSRF_TRUSTED_ORIGINS = ['https://vrtfund.com','https://www.vrtfund.com']

MEDIA_ROOT = '/var/www/vrt/media/'
MEDIA_URL = '/media/'