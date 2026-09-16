"""
ASGI config for backend_django project.

It exposes the ASGI callable as a module-level variable named
'application'.
"""


from core.debug_console.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend_django.settings",
)


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            websocket_urlpatterns
        ),
    }
)
