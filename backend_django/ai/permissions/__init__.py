"""
AI permissions package.

Compatibility exports for existing imports:
from ai.permissions import AIAuthenticatedPermission
"""

from ..services.permissions import AIAuthenticatedPermission

__all__ = [
    "AIAuthenticatedPermission",
]