# automation/engine/registry.py

ACTION_REGISTRY = {}


def register_action(name):
    def decorator(cls):
        ACTION_REGISTRY[name] = cls()
        return cls
    return decorator


def get_action(name):
    action = ACTION_REGISTRY.get(name)
    if not action:
        raise Exception(f"Unknown action {name}")
    return action
