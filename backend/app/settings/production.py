from .base import *

DEBUG = False
ALLOWED_HOSTS = get_config('ALLOWED_HOSTS', default='').split(',')
