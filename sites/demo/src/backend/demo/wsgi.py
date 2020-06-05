"""
WSGI config for the funmooc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "funmooc.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

application = get_wsgi_application()
