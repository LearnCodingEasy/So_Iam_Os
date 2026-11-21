from __future__ import annotations
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from personal_finance.models import FinancialAlert, FinancialScenario
from personal_finance.api.serializers import FinancialAlertSerializer
from personal_finance.services import alerts_for_user, coach_answer, daily_summary, ecosystem_integration, financial_health, forecast, period_report, scenario


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health(request):
    return Response(financial_health(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def forecast_view(request):
    months = min(max(int(request.query_params.get("months", 3)), 1), 24)
    return Response(forecast(request.user, months))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def scenario_view(request):
    result = scenario(
        request.user,
        request.data.get("income_change_percent", 0),
        request.data.get("expense_change_percent", 0),
        request.data.get("extra_debt_payment", 0),
        request.data.get("case", "expected"),
    )
    FinancialScenario.objects.create(
        user=request.user,
        name=request.data.get("name", "Scenario"),
        income_change_percent=request.data.get("income_change_percent", 0),
        expense_change_percent=request.data.get("expense_change_percent", 0),
        debt_payment_extra=request.data.get("extra_debt_payment", 0),
        case=request.data.get("case", "expected"),
        result=result,
    )
    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def daily_summary_view(request):
    return Response(daily_summary(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def report_view(request, period):
    if period not in ("weekly", "monthly"):
        return Response({"detail": "Period must be weekly or monthly."}, status=400)
    return Response(period_report(request.user, period))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def coach_view(request):
    question = request.data.get("question", "").strip()
    if not question:
        return Response({"detail": "Question is required."}, status=400)
    return Response({
        "disclaimer": "AI financial coaching is informational planning assistance, not professional financial advice.",
        "answer": coach_answer(request.user, question),
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_alerts_view(request):
    alerts_for_user(request.user)
    return Response(FinancialAlertSerializer(FinancialAlert.objects.filter(user=request.user, read=False), many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ecosystem_view(request):
    return Response(ecosystem_integration(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_contract_view(request):
    prefix = "/api/finance/"
    paths = [
        "categories/", "transactions/", "transactions/summary/", "transactions/dashboard/",
        "transactions/insights/", "transactions/history/", "transactions/spending/", "transactions/ai_insights/",
        "budgets/", "debts/", "debts/{id}/payments/", "debts/{id}/pay/", "savings-goals/", "savings-goals/{id}/plan/",
        "subscriptions/", "debt-payments/", "loans/", "loans/{id}/pay/", "loan-payments/", "recurring-cashflows/",
        "profile/", "habits/", "alerts/", "alerts/{id}/mark_read/", "scenarios/", "health/", "forecast/",
        "forecast/scenario/", "daily-summary/", "reports/weekly/", "reports/monthly/", "ai/coach/",
        "alerts/refresh/", "ecosystem/", "contract/",
    ]
    return Response({"prefix": prefix, "endpoints": [prefix + p for p in paths], "authenticated": True})
