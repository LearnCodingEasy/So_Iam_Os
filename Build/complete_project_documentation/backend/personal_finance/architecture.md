# personal_finance architecture

## Module structure
- Models: 16 Python files under models/.
- API: 36 Python files under api/.
- Services: 2 Python files under services/.
- Tests: 2; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/budget_serializers.py
api/serializers/category_serializers.py
api/serializers/debt_payment_serializers.py
api/serializers/debt_serializers.py
api/serializers/financial_alert_serializers.py
api/serializers/financial_habit_serializers.py
api/serializers/financial_profile_serializers.py
api/serializers/financial_scenario_serializers.py
api/serializers/lending_borrowing_serializers.py
api/serializers/loan_payment_serializers.py
api/serializers/owned_model_serializers.py
api/serializers/recurring_cashflow_serializers.py
api/serializers/savings_goal_serializers.py
api/serializers/saving_plan_serializers.py
api/serializers/subscription_serializers.py
api/serializers/transaction_serializers.py
api/serializers/__init__.py
api/views/budget_views.py
api/views/category_views.py
api/views/common.py
api/views/debt_payment_views.py
api/views/debt_views.py
api/views/financial_alert_views.py
api/views/financial_habit_views.py
api/views/financial_profile_views.py
api/views/financial_scenario_views.py
api/views/lending_borrowing_views.py
api/views/loan_payment_views.py
api/views/owned_views.py
api/views/recurring_cashflow_views.py
api/views/savings_goal_views.py
api/views/subscription_views.py
api/views/transaction_views.py
api/views/__init__.py

### models
models/budget.py
models/category.py
models/debt.py
models/debt_payment.py
models/financial_alert.py
models/financial_habit.py
models/financial_profile.py
models/financial_scenario.py
models/lending_borrowing.py
models/loan_payment.py
models/recurring_cashflow.py
models/savings_goal.py
models/saving_plan.py
models/subscription.py
models/transaction.py
models/__init__.py

### services
services/personal_finance_services.py
services/__init__.py

### tests
tests/test_personal_finance.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
