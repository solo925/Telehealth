"""
This is the ASGI (Asynchronous Server Gateway Interface) configuration for the Telehealth Django project. It sets up the routing for the WebSocket protocol, using the AuthMiddlewareStack to handle authentication, and the URLRouter to map WebSocket URLs to the appropriate routing handlers.

The ProtocolTypeRouter is used to handle both HTTP and WebSocket protocols. The HTTP protocol is handled by the Django ASGI application, while the WebSocket protocol is handled by the AuthMiddlewareStack and URLRouter, which maps the WebSocket URLs to the routing handlers defined in the consultations.routing module.
"""
# Telehealth/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import consultations.routing  # or your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Telehealth.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            consultations.routing.websocket_urlpatterns
        )
    ),
})

