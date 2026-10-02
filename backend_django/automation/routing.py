from django.urls import re_path
from .consumers import WorkflowLogConsumer

websocket_urlpatterns = [
    re_path(r'ws/workflow/(?P<task_run_id>\w+)/$',
            WorkflowLogConsumer.as_asgi()),
]
