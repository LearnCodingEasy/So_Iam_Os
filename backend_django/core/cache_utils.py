from django.core.cache import cache

def invalidate_dashboard(user_id):
    try:
        cache.delete(f"dashboard:{user_id}")
    except Exception:
        pass
