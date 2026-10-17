from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, TransactionViewSet, BudgetViewSet, DebtViewSet, SavingsGoalViewSet,
    SubscriptionViewSet, DebtPaymentViewSet, LendingBorrowingViewSet, LoanPaymentViewSet,
    RecurringCashflowViewSet, FinancialProfileViewSet, FinancialHabitViewSet,
    FinancialAlertViewSet, FinancialScenarioViewSet, health, forecast_view, scenario_view,
    daily_summary_view, report_view, coach_view, refresh_alerts_view, api_contract_view, ecosystem_view,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="finance-category")
router.register("transactions", TransactionViewSet, basename="finance-transaction")
router.register("budgets", BudgetViewSet, basename="finance-budget")
router.register("debts", DebtViewSet, basename="finance-debt")
router.register("savings-goals", SavingsGoalViewSet, basename="finance-savings")
router.register("subscriptions", SubscriptionViewSet, basename="finance-subscription")
router.register("debt-payments", DebtPaymentViewSet, basename="finance-debt-payment")
router.register("loans", LendingBorrowingViewSet, basename="finance-loan")
router.register("loan-payments", LoanPaymentViewSet, basename="finance-loan-payment")
router.register("recurring-cashflows", RecurringCashflowViewSet, basename="finance-recurring-cashflow")
router.register("profile", FinancialProfileViewSet, basename="finance-profile")
router.register("habits", FinancialHabitViewSet, basename="finance-habit")
router.register("alerts", FinancialAlertViewSet, basename="finance-alert")
router.register("scenarios", FinancialScenarioViewSet, basename="finance-scenario")

urlpatterns = [
    path("health/", health, name="finance-health"),
    path("forecast/", forecast_view, name="finance-forecast"),
    path("forecast/scenario/", scenario_view, name="finance-forecast-scenario"),
    path("daily-summary/", daily_summary_view, name="finance-daily-summary"),
    path("reports/<str:period>/", report_view, name="finance-report"),
    path("ai/coach/", coach_view, name="finance-ai-coach"),
    path("alerts/refresh/", refresh_alerts_view, name="finance-alerts-refresh"),
    path("ecosystem/", ecosystem_view, name="finance-ecosystem"),
    path("contract/", api_contract_view, name="finance-api-contract"),
]
urlpatterns += router.urls
