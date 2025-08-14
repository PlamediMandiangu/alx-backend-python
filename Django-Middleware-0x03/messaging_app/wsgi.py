"""
WSGI config for messaging_app project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information, see:
https://docs.djangoproject.com/en/4.3/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

# WSGI application
application = get_wsgi_application()
