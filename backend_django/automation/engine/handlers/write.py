# automation/engine/handlers/write.py

from ..registry import register_action


@register_action("write")
class WriteAction:

    def execute(self, payload):
        print("write", payload)
        return True
