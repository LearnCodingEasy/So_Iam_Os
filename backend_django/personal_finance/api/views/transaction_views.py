from __future__ import annotations
from datetime import date
from rest_framework.decorators import action
from rest_framework.response import Response
from personal_finance.models import Transaction
from personal_finance.api.serializers import TransactionSerializer
from personal_finance.services import dashboard, insights, spending_breakdown
from personal_finance.api.views.owned_views import Owned


class TransactionViewSet(Owned):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.select_related("category").all()

    @action(detail=False, methods=["get"])
    def summary(self, request):
        return Response(dashboard(request.user))

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        return Response(dashboard(request.user))

    @action(detail=False, methods=["get"])
    def insights(self, request):
        return Response(insights(request.user))

    @action(detail=False, methods=["get"])
    def history(self, request):
        start = request.query_params.get("from")
        end = request.query_params.get("to")
        try:
            parsed_start = date.fromisoformat(start) if start else None
            parsed_end = date.fromisoformat(end) if end else None
        except ValueError:
            return Response({"detail": "Invalid date. Use YYYY-MM-DD."}, status=400)
        return Response(dashboard(request.user, parsed_start, parsed_end))

    @action(detail=False, methods=["get"])
    def spending(self, request):
        return Response(spending_breakdown(request.user))

    @action(detail=False, methods=["post"])
    def ai_insights(self, request):
        if not request.data.get("share_with_ai"):
            return Response(
                {"requires_confirmation": True, "message": "Confirm that you want to share the selected financial summary with the configured AI provider."},
                status=400,
            )
        from ai.services import AIService
        import json
        prompt = (
            "Analyze this personal-finance summary as informational planning assistance only. "
            "Do not provide regulated financial advice. Return 3 concise observations and 3 practical next steps.\n"
            + json.dumps(dashboard(request.user), default=str, ensure_ascii=False)
        )
        try:
            result = AIService(request.user).chat(prompt)
            return Response({
                "disclaimer": "Informational planning assistance only; not licensed financial advice.",
                "provider": result.get("provider"),
                "model": result.get("model"),
                "content": result["assistant_message"].content,
            })
        except Exception:
            return Response({
                "disclaimer": "Informational planning assistance only; not licensed financial advice.",
                "fallback": insights(request.user),
                "message": "AI provider is unavailable. The local financial analysis is still available.",
            }, status=200)
