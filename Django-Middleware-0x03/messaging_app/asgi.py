"""
ASGI config for messaging_app project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information, see:
https://docs.djangoproject.com/en/4.3/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

# ASGI application
application = get_asgi_application()
