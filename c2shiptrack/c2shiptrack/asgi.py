"""
ASGI config for c2shiptrack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c2shiptrack.settings')
# django.setup()
# application = get_default_application()

application = get_asgi_application()
# channel_layer = get_channel_layer()
