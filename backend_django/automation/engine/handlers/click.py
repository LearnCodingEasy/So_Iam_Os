# automation/engine/handlers/click.py

from ..registry import register_action


@register_action("click")
class ClickAction:

    def execute(self, payload):
        print("click", payload)
        return True
