from .common import *  # noqa

SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
