from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Category, Transaction, Budget, Debt, DebtPayment, LendingBorrowing, LoanPayment,
    SavingsGoal, SavingPlan, Subscription, RecurringCashflow, FinancialProfile,
    FinancialHabit, FinancialAlert, FinancialScenario,
)
from .serializers import (
    CategorySerializer, TransactionSerializer, BudgetSerializer, DebtSerializer,
    DebtPaymentSerializer, LendingBorrowingSerializer, LoanPaymentSerializer,
    SavingsGoalSerializer, SavingPlanSerializer, SubscriptionSerializer,
    RecurringCashflowSerializer, FinancialProfileSerializer, FinancialHabitSerializer,
    FinancialAlertSerializer, FinancialScenarioSerializer,
)
from .services import (
    alerts_for_user, coach_answer, dashboard, daily_summary, ecosystem_integration, financial_health,
    forecast, insights, period_report, scenario, spending_breakdown,
)


class Owned(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CategoryViewSet(Owned):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


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


class BudgetViewSet(Owned):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.select_related("category").all()


class DebtViewSet(Owned):
    serializer_class = DebtSerializer
    queryset = Debt.objects.all()

    @action(detail=True, methods=["get"])
    def payments(self, request, pk=None):
        debt = self.get_object()
        return Response(DebtPaymentSerializer(debt.payments.all(), many=True).data)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        debt = self.get_object()
        amount = Decimal(str(request.data.get("amount", "0")))
        if amount <= 0:
            return Response({"detail": "Payment amount must be positive."}, status=400)
        if amount > debt.balance:
            return Response({"detail": "Payment cannot exceed the remaining debt balance."}, status=400)
        paid_on = request.data.get("paid_on") or timezone.localdate()
        note = request.data.get("note", "")
        with db_transaction.atomic():
            tx = Transaction.objects.create(
                user=request.user, kind="debt_payment", amount=amount, currency=debt.currency,
                occurred_on=paid_on, description=f"Debt payment: {debt.name}",
            )
            payment = DebtPayment.objects.create(user=request.user, debt=debt, amount=amount, paid_on=paid_on, note=note, transaction=tx)
            debt.balance = debt.balance - amount
            if debt.balance <= 0:
                debt.balance = 0
                debt.status = "paid"
            debt.save(update_fields=["balance", "status"])
        return Response(DebtPaymentSerializer(payment).data, status=201)


class SavingsGoalViewSet(Owned):
    serializer_class = SavingsGoalSerializer
    queryset = SavingsGoal.objects.all()

    @action(detail=True, methods=["get", "post"])
    def plan(self, request, pk=None):
        goal = self.get_object()
        if request.method == "GET":
            plan = getattr(goal, "plan", None)
            if not plan:
                return Response({"detail": "No saving plan yet."}, status=404)
            return Response(SavingPlanSerializer(plan).data)
        from django.utils import timezone as tz
        today = tz.localdate()
        remaining = max(Decimal("0"), goal.target_amount - goal.current_amount)
        days = max(1, (goal.target_date - today).days) if goal.target_date else 30
        daily = remaining / Decimal(days)
        weekly = daily * 7
        monthly = daily * 30
        plan, _ = SavingPlan.objects.update_or_create(
            goal=goal, defaults={"user": request.user, "daily_amount": daily, "weekly_amount": weekly, "monthly_amount": monthly, "expected_completion": goal.target_date}
        )
        return Response(SavingPlanSerializer(plan).data)


class SubscriptionViewSet(Owned):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class DebtPaymentViewSet(Owned):
    serializer_class = DebtPaymentSerializer
    queryset = DebtPayment.objects.select_related("debt").all()


class LendingBorrowingViewSet(Owned):
    serializer_class = LendingBorrowingSerializer
    queryset = LendingBorrowing.objects.all()

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        loan = self.get_object()
        amount = Decimal(str(request.data.get("amount", "0")))
        if amount <= 0 or amount > loan.remaining:
            return Response({"detail": "Payment amount must be positive and cannot exceed remaining amount."}, status=400)
        with db_transaction.atomic():
            LoanPayment.objects.create(
                user=request.user, loan=loan, amount=amount,
                paid_on=request.data.get("paid_on") or timezone.localdate(),
                note=request.data.get("note", ""),
            )
            loan.remaining -= amount
            loan.status = "paid" if loan.remaining <= 0 else "partial"
            loan.save(update_fields=["remaining", "status"])
        return Response(LendingBorrowingSerializer(loan).data)


class LoanPaymentViewSet(Owned):
    serializer_class = LoanPaymentSerializer
    queryset = LoanPayment.objects.select_related("loan").all()


class RecurringCashflowViewSet(Owned):
    serializer_class = RecurringCashflowSerializer
    queryset = RecurringCashflow.objects.all()


class FinancialProfileViewSet(Owned):
    serializer_class = FinancialProfileSerializer
    queryset = FinancialProfile.objects.all()


class FinancialHabitViewSet(Owned):
    serializer_class = FinancialHabitSerializer
    queryset = FinancialHabit.objects.all()


class FinancialAlertViewSet(Owned):
    serializer_class = FinancialAlertSerializer
    queryset = FinancialAlert.objects.all()

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        alert = self.get_object()
        alert.read = True
        alert.save(update_fields=["read"])
        return Response(FinancialAlertSerializer(alert).data)


class FinancialScenarioViewSet(Owned):
    serializer_class = FinancialScenarioSerializer
    queryset = FinancialScenario.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        instance.result = scenario(
            self.request.user,
            instance.income_change_percent,
            instance.expense_change_percent,
            instance.debt_payment_extra,
            instance.case,
        )
        instance.save(update_fields=["result"])


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
