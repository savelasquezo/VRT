from .settings  import *

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["167.71.28.44","vrtfund.com","www.vrtfund.com"]

CSRF_TRUSTED_ORIGINS = ['https://vrtfund.com','https://www.vrtfund.com']

MEDIA_ROOT = os.path.join(BASE_DIR, '')
MEDIA_URL = '/'
