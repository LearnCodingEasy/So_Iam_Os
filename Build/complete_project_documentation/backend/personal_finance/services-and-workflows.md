# personal_finance services and workflows

## Service/task/signal source


### personal_finance/services/personal_finance_services.py
L14: def profile_for(user):
L19: def _money(value):
L23: def _range_for_period(today, period="month"):
L34: def _totals(qs):
L43: def dashboard(user, start=None, end=None):
L90: def summary(user):
L95: def spending_breakdown(user, start=None, end=None):
L108: def financial_health(user):
L169: def _goal_progress(user):
L181: def forecast(user, months=3):
L215: def _goal_projection(user, surplus):
L227: def scenario(user, income_change=0, expense_change=0, extra_debt_payment=0, case="expected"):
L244: def alerts_for_user(user):
L271: def insights(user):
L293: def daily_summary(user):
L298: def period_report(user, period="monthly"):
L319: def coach_answer(user, question):
L334: def ecosystem_integration(user):

### personal_finance/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
