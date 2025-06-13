"""
WSGI config for codebysiri project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codebysiri.settings')

application = get_wsgi_application()
