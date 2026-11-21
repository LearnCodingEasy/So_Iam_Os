# personal_finance API

Project prefix: /api/finance/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: personal_finance/api/urls.py

- L7: router.register("categories", CategoryViewSet, basename="finance-category")

- L8: router.register("transactions", TransactionViewSet, basename="finance-transaction")

- L9: router.register("budgets", BudgetViewSet, basename="finance-budget")

- L10: router.register("debts", DebtViewSet, basename="finance-debt")

- L11: router.register("savings-goals", SavingsGoalViewSet, basename="finance-savings")

- L12: router.register("subscriptions", SubscriptionViewSet, basename="finance-subscription")

- L13: router.register("debt-payments", DebtPaymentViewSet, basename="finance-debt-payment")

- L14: router.register("loans", LendingBorrowingViewSet, basename="finance-loan")

- L15: router.register("loan-payments", LoanPaymentViewSet, basename="finance-loan-payment")

- L16: router.register("recurring-cashflows", RecurringCashflowViewSet, basename="finance-recurring-cashflow")

- L17: router.register("profile", FinancialProfileViewSet, basename="finance-profile")

- L18: router.register("habits", FinancialHabitViewSet, basename="finance-habit")

- L19: router.register("alerts", FinancialAlertViewSet, basename="finance-alert")

- L20: router.register("scenarios", FinancialScenarioViewSet, basename="finance-scenario")

- L23: path("health/", health, name="finance-health"),

- L24: path("forecast/", forecast_view, name="finance-forecast"),

- L25: path("forecast/scenario/", scenario_view, name="finance-forecast-scenario"),

- L26: path("daily-summary/", daily_summary_view, name="finance-daily-summary"),

- L27: path("reports/<str:period>/", report_view, name="finance-report"),

- L28: path("ai/coach/", coach_view, name="finance-ai-coach"),

- L29: path("alerts/refresh/", refresh_alerts_view, name="finance-alerts-refresh"),

- L30: path("ecosystem/", ecosystem_view, name="finance-ecosystem"),

- L31: path("contract/", api_contract_view, name="finance-api-contract"),

## Handler declarations: personal_finance/api/views/budget_views.py
L7: class BudgetViewSet(Owned):
L8: serializer_class = BudgetSerializer

## Handler declarations: personal_finance/api/views/category_views.py
L7: class CategoryViewSet(Owned):
L8: serializer_class = CategorySerializer

## Handler declarations: personal_finance/api/views/common.py
L2: from rest_framework.decorators import api_view, permission_classes
L11: @permission_classes([IsAuthenticated])
L17: @permission_classes([IsAuthenticated])
L24: @permission_classes([IsAuthenticated])
L46: @permission_classes([IsAuthenticated])
L52: @permission_classes([IsAuthenticated])
L60: @permission_classes([IsAuthenticated])
L72: @permission_classes([IsAuthenticated])
L79: @permission_classes([IsAuthenticated])
L85: @permission_classes([IsAuthenticated])

## Handler declarations: personal_finance/api/views/debt_payment_views.py
L7: class DebtPaymentViewSet(Owned):
L8: serializer_class = DebtPaymentSerializer

## Handler declarations: personal_finance/api/views/debt_views.py
L12: class DebtViewSet(Owned):
L13: serializer_class = DebtSerializer
L16: @action(detail=True, methods=["get"])
L21: @action(detail=True, methods=["post"])

## Handler declarations: personal_finance/api/views/financial_alert_views.py
L9: class FinancialAlertViewSet(Owned):
L10: serializer_class = FinancialAlertSerializer
L13: @action(detail=True, methods=["post"])

## Handler declarations: personal_finance/api/views/financial_habit_views.py
L7: class FinancialHabitViewSet(Owned):
L8: serializer_class = FinancialHabitSerializer

## Handler declarations: personal_finance/api/views/financial_profile_views.py
L7: class FinancialProfileViewSet(Owned):
L8: serializer_class = FinancialProfileSerializer

## Handler declarations: personal_finance/api/views/financial_scenario_views.py
L8: class FinancialScenarioViewSet(Owned):
L9: serializer_class = FinancialScenarioSerializer
L12: def perform_create(self, serializer):

## Handler declarations: personal_finance/api/views/lending_borrowing_views.py
L12: class LendingBorrowingViewSet(Owned):
L13: serializer_class = LendingBorrowingSerializer
L16: @action(detail=True, methods=["post"])

## Handler declarations: personal_finance/api/views/loan_payment_views.py
L7: class LoanPaymentViewSet(Owned):
L8: serializer_class = LoanPaymentSerializer

## Handler declarations: personal_finance/api/views/owned_views.py
L3: from rest_framework.decorators import permission_classes
L7: class Owned(viewsets.ModelViewSet):
L8: permission_classes = [IsAuthenticated]
L10: def perform_create(self, serializer):
L13: def get_queryset(self):

## Handler declarations: personal_finance/api/views/recurring_cashflow_views.py
L7: class RecurringCashflowViewSet(Owned):
L8: serializer_class = RecurringCashflowSerializer

## Handler declarations: personal_finance/api/views/savings_goal_views.py
L10: class SavingsGoalViewSet(Owned):
L11: serializer_class = SavingsGoalSerializer
L14: @action(detail=True, methods=["get", "post"])

## Handler declarations: personal_finance/api/views/subscription_views.py
L7: class SubscriptionViewSet(Owned):
L8: serializer_class = SubscriptionSerializer

## Handler declarations: personal_finance/api/views/transaction_views.py
L11: class TransactionViewSet(Owned):
L12: serializer_class = TransactionSerializer
L15: @action(detail=False, methods=["get"])
L19: @action(detail=False, methods=["get"])
L23: @action(detail=False, methods=["get"])
L27: @action(detail=False, methods=["get"])
L38: @action(detail=False, methods=["get"])
L42: @action(detail=False, methods=["post"])


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
