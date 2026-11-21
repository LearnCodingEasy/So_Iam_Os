# personal_finance source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## personal_finance/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin; from .models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/apps.py
- Type/area: Python module
- Definitions: class PersonalFinanceConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path; from rest_framework.routers import DefaultRouter; from personal_finance.api.views import CategoryViewSet, TransactionViewSet, BudgetViewSet, DebtViewSet, SavingsGoalViewSet, SubscriptionViewSet, DebtPaymentViewSet, LendingBorrowingViewSet, LoanPaymentViewSet, RecurringCashflowViewSet, FinancialProfileViewSet, FinancialHabitViewSet, FinancialAlertViewSet, FinancialScenarioViewSet, health, forecast_view, scenario_view, daily_summary_view, report_view, coach_view, refresh_alerts_view, api_contract_view, ecosystem_view
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/budget_serializers.py
- Type/area: Python API source
- Definitions: class BudgetSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import Budget; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/category_serializers.py
- Type/area: Python API source
- Definitions: class CategorySerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import Category; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/debt_payment_serializers.py
- Type/area: Python API source
- Definitions: class DebtPaymentSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import DebtPayment; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/debt_serializers.py
- Type/area: Python API source
- Definitions: class DebtSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import Debt; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/financial_alert_serializers.py
- Type/area: Python API source
- Definitions: class FinancialAlertSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import FinancialAlert; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/financial_habit_serializers.py
- Type/area: Python API source
- Definitions: class FinancialHabitSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import FinancialHabit; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/financial_profile_serializers.py
- Type/area: Python API source
- Definitions: class FinancialProfileSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import FinancialProfile; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/financial_scenario_serializers.py
- Type/area: Python API source
- Definitions: class FinancialScenarioSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import FinancialScenario; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/lending_borrowing_serializers.py
- Type/area: Python API source
- Definitions: class LendingBorrowingSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import LendingBorrowing; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/loan_payment_serializers.py
- Type/area: Python API source
- Definitions: class LoanPaymentSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import LoanPayment; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/owned_model_serializers.py
- Type/area: Python API source
- Definitions: class OwnedModelSerializer(serializers.ModelSerializer):; class Meta:; def validate_category(self, category):
- Imports (first four): from rest_framework import serializers
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/recurring_cashflow_serializers.py
- Type/area: Python API source
- Definitions: class RecurringCashflowSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import RecurringCashflow; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/savings_goal_serializers.py
- Type/area: Python API source
- Definitions: class SavingsGoalSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import SavingsGoal; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/saving_plan_serializers.py
- Type/area: Python API source
- Definitions: class SavingPlanSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import SavingPlan; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/subscription_serializers.py
- Type/area: Python API source
- Definitions: class SubscriptionSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):
- Imports (first four): from personal_finance.models import Subscription; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/transaction_serializers.py
- Type/area: Python API source
- Definitions: class TransactionSerializer(OwnedModelSerializer):; class Meta(OwnedModelSerializer.Meta):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from personal_finance.models import Transaction; from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .owned_model_serializers import OwnedModelSerializer; from .category_serializers import CategorySerializer; from .transaction_serializers import TransactionSerializer; from .budget_serializers import BudgetSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/budget_views.py
- Type/area: Python API source
- Definitions: class BudgetViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import Budget; from personal_finance.api.serializers import BudgetSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/category_views.py
- Type/area: Python API source
- Definitions: class CategoryViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import Category; from personal_finance.api.serializers import CategorySerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/common.py
- Type/area: Python API source
- Definitions: def health(request):; def forecast_view(request):; def scenario_view(request):; def daily_summary_view(request):; def report_view(request, period):; def coach_view(request):; def refresh_alerts_view(request):; def ecosystem_view(request):; def api_contract_view(request):
- Imports (first four): from __future__ import annotations; from rest_framework.decorators import api_view, permission_classes; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/debt_payment_views.py
- Type/area: Python API source
- Definitions: class DebtPaymentViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import DebtPayment; from personal_finance.api.serializers import DebtPaymentSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/debt_views.py
- Type/area: Python API source
- Definitions: class DebtViewSet(Owned):; def payments(self, request, pk=None):; def pay(self, request, pk=None):
- Imports (first four): from __future__ import annotations; from decimal import Decimal; from django.db import transaction as db_transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/financial_alert_views.py
- Type/area: Python API source
- Definitions: class FinancialAlertViewSet(Owned):; def mark_read(self, request, pk=None):
- Imports (first four): from __future__ import annotations; from rest_framework.decorators import action; from rest_framework.response import Response; from personal_finance.models import FinancialAlert
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/financial_habit_views.py
- Type/area: Python API source
- Definitions: class FinancialHabitViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import FinancialHabit; from personal_finance.api.serializers import FinancialHabitSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/financial_profile_views.py
- Type/area: Python API source
- Definitions: class FinancialProfileViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import FinancialProfile; from personal_finance.api.serializers import FinancialProfileSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/financial_scenario_views.py
- Type/area: Python API source
- Definitions: class FinancialScenarioViewSet(Owned):; def perform_create(self, serializer):
- Imports (first four): from __future__ import annotations; from personal_finance.models import FinancialScenario; from personal_finance.api.serializers import FinancialScenarioSerializer; from personal_finance.services import scenario
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/lending_borrowing_views.py
- Type/area: Python API source
- Definitions: class LendingBorrowingViewSet(Owned):; def pay(self, request, pk=None):
- Imports (first four): from __future__ import annotations; from decimal import Decimal; from django.db import transaction as db_transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/loan_payment_views.py
- Type/area: Python API source
- Definitions: class LoanPaymentViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import LoanPayment; from personal_finance.api.serializers import LoanPaymentSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/owned_views.py
- Type/area: Python API source
- Definitions: class Owned(viewsets.ModelViewSet):; def perform_create(self, serializer):; def get_queryset(self):
- Imports (first four): from __future__ import annotations; from rest_framework import viewsets; from rest_framework.decorators import permission_classes; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/recurring_cashflow_views.py
- Type/area: Python API source
- Definitions: class RecurringCashflowViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import RecurringCashflow; from personal_finance.api.serializers import RecurringCashflowSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/savings_goal_views.py
- Type/area: Python API source
- Definitions: class SavingsGoalViewSet(Owned):; def plan(self, request, pk=None):
- Imports (first four): from __future__ import annotations; from decimal import Decimal; from rest_framework.decorators import action; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/subscription_views.py
- Type/area: Python API source
- Definitions: class SubscriptionViewSet(Owned):
- Imports (first four): from __future__ import annotations; from personal_finance.models import Subscription; from personal_finance.api.serializers import SubscriptionSerializer; from personal_finance.api.views.owned_views import Owned
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/transaction_views.py
- Type/area: Python API source
- Definitions: class TransactionViewSet(Owned):; def summary(self, request):; def dashboard(self, request):; def insights(self, request):; def history(self, request):; def spending(self, request):; def ai_insights(self, request):
- Imports (first four): from __future__ import annotations; from datetime import date; from rest_framework.decorators import action; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .owned_views import Owned; from .category_views import CategoryViewSet; from .transaction_views import TransactionViewSet; from .budget_views import BudgetViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/budget.py
- Type/area: Python model source
- Definitions: class Budget(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/category.py
- Type/area: Python model source
- Definitions: class Category(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/debt.py
- Type/area: Python model source
- Definitions: class Debt(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/debt_payment.py
- Type/area: Python model source
- Definitions: class DebtPayment(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/financial_alert.py
- Type/area: Python model source
- Definitions: class FinancialAlert(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/financial_habit.py
- Type/area: Python model source
- Definitions: class FinancialHabit(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/financial_profile.py
- Type/area: Python model source
- Definitions: class FinancialProfile(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/financial_scenario.py
- Type/area: Python model source
- Definitions: class FinancialScenario(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/lending_borrowing.py
- Type/area: Python model source
- Definitions: class LendingBorrowing(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/loan_payment.py
- Type/area: Python model source
- Definitions: class LoanPayment(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/recurring_cashflow.py
- Type/area: Python model source
- Definitions: class RecurringCashflow(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/savings_goal.py
- Type/area: Python model source
- Definitions: class SavingsGoal(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/saving_plan.py
- Type/area: Python model source
- Definitions: class SavingPlan(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.db import models; from personal_finance.models.savings_goal import SavingsGoal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/subscription.py
- Type/area: Python model source
- Definitions: class Subscription(models.Model):
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/transaction.py
- Type/area: Python model source
- Definitions: class Transaction(models.Model):; class Meta:
- Imports (first four): from __future__ import annotations; from django.conf import settings; from django.core.validators import MinValueValidator; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .category import Category; from .transaction import Transaction; from .budget import Budget; from .debt import Debt
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/services/personal_finance_services.py
- Type/area: Python service source
- Definitions: def profile_for(user):; def _money(value):; def _range_for_period(today, period="month"):; def _totals(qs):; def dashboard(user, start=None, end=None):; def summary(user):; def spending_breakdown(user, start=None, end=None):; def financial_health(user):; def _goal_progress(user):; def forecast(user, months=3):; def _goal_projection(user, surplus):; def scenario(user, income_change=0, expense_change=0, extra_debt_payment=0, case="expected"):; def alerts_for_user(user):; def insights(user):; def daily_summary(user):; def period_report(user, period="monthly"):; def coach_answer(user, question):; def ecosystem_integration(user):
- Imports (first four): from __future__ import annotations; from calendar import monthrange; from datetime import date, timedelta; from decimal import Decimal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .personal_finance_services import ZERO, profile_for, _money, _range_for_period, _totals, dashboard, summary, spending_breakdown, financial_health, _goal_progress, forecast, _goal_projection, scenario, alerts_for_user, insights, daily_summary, period_report, coach_answer, ecosystem_integration
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/tests/test_personal_finance.py
- Type/area: Python test source
- Definitions: class FinanceAPITestCase(APITestCase):; def setUp(self):; def test_dashboard_is_user_scoped(self):; def test_foreign_category_is_rejected(self):; def test_health_forecast_reports_and_contract(self):; def test_debt_payment_reduces_balance_and_creates_transaction(self):; def test_user_cannot_see_other_users_data(self):
- Imports (first four): from datetime import date, timedelta; from decimal import Decimal; from django.urls import reverse; from rest_framework.test import APITestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## personal_finance/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

