"""
Shared constants used across So_Iam_OS.
"""


# ----------------------------------------------------
# General
# ----------------------------------------------------


APP_NAME = "So_Iam_OS"

APP_VERSION = "1.0.0"


# ----------------------------------------------------
# Object Status
# ----------------------------------------------------


STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_ARCHIVED = "archived"
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


COMMON_STATUSES = (
    (STATUS_ACTIVE, "Active"),
    (STATUS_INACTIVE, "Inactive"),
    (STATUS_ARCHIVED, "Archived"),
    (STATUS_PENDING, "Pending"),
    (STATUS_COMPLETED, "Completed"),
    (STATUS_FAILED, "Failed"),
)


# ----------------------------------------------------
# Generic limits
# ----------------------------------------------------


DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# ----------------------------------------------------
# API
# ----------------------------------------------------


API_SUCCESS = "success"
API_ERROR = "error"
