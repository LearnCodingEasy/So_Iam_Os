import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.exceptions import AIError
from ai.permissions import AIAuthenticatedPermission
from ai.services.business_insights import (
    NoBusinessDataError, collect_business_snapshot, generate_business_insight,
)
from ai.services.timeouts import validate_timeout

logger = logging.getLogger(__name__)


class AIBusinessInsightView(APIView):
    """GET: the real aggregated snapshot (no AI). POST: AI analysis of it."""
    permission_classes = [AIAuthenticatedPermission]

    def get(self, request):
        snapshot, has_data = collect_business_snapshot(request.user)
        return Response({"success": True, "has_data": has_data, "snapshot": snapshot})

    def post(self, request):
        raw = request.data.get("timeout", request.data.get("timeout_seconds"))
        timeout = None
        if raw not in (None, ""):
            try:
                timeout = validate_timeout(raw)
            except ValueError as exc:
                return Response({"success": False, "error": str(exc), "field": "timeout"}, status=400)
        try:
            data = generate_business_insight(
                request.user,
                provider=(request.data.get("provider") or None),
                model=(request.data.get("model") or None),
                timeout_seconds=timeout,
            )
        except NoBusinessDataError as exc:
            return Response({"success": False, "error": str(exc), "error_code": exc.category},
                            status=status.HTTP_409_CONFLICT)
        except AIError as exc:
            code = getattr(exc, "category", "ai_error")
            return Response(
                {"success": False, "error": str(exc), "error_code": code,
                 "timeout_kind": getattr(exc, "timeout_kind", None),
                 "retryable": bool(getattr(exc, "retryable", False))},
                status=status.HTTP_504_GATEWAY_TIMEOUT if code == "timeout" else status.HTTP_502_BAD_GATEWAY,
            )
        except Exception:
            logger.exception("Business insight failed for user %s", request.user.pk)
            return Response({"success": False, "error": "An unexpected AI error occurred."}, status=500)
        return Response({"success": True, **data})
