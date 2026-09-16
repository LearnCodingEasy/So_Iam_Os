from django.urls import re_path

from .consumers import DebugConsoleConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/debug/$",
        DebugConsoleConsumer.as_asgi(),
    ),
]
