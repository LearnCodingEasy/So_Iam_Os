# automation/engine/executor.py

from .registry import get_action


class ActionExecutor:

    def execute(self, action):
        handler = get_action(action.action_type)
        return handler.execute(action.payload)
