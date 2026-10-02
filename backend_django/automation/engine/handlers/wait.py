# automation/engine/handlers/wait.py

import time
from ..registry import register_action


@register_action("wait")
class WaitAction:

    def execute(self, payload):
        time.sleep(payload.get("seconds", 1))
        return True
