import json
from urllib.parse import urlparse
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

class DebugConsoleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not getattr(settings, "SO_IAM_OS_DEBUG_CONSOLE", False):
            await self.close(code=4403); return
        origin = next((v.decode() for k,v in self.scope.get("headers", []) if k == b"origin"), "")
        allowed = set(getattr(settings, "CORS_ALLOWED_ORIGINS", []))
        if origin and allowed and origin not in allowed:
            await self.close(code=4403); return
        self.group_name = "debug_console"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"type":"system","level":"success","message":"Debug Console connected"}))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_log(self, event):
        await self.send(text_data=json.dumps(event["data"]))
