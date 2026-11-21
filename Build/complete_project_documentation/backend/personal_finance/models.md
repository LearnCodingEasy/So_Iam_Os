# personal_finance models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## budget
Source: personal_finance/models/budget.py

- L8: class Budget(models.Model):

- L11: name = models.CharField(max_length=150)

- L12: period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="monthly")

- L13: limit_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L14: currency = models.CharField(max_length=10, default="USD")

- L16: active = models.BooleanField(default=True)

## category
Source: personal_finance/models/category.py

- L6: class Category(models.Model):

- L14: name = models.CharField(max_length=120)

- L15: kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="expense")

- L17: class Meta:

- L18: constraints = [

- L19: models.UniqueConstraint(fields=["user", "name", "kind"], name="finance_category_unique"),

## debt
Source: personal_finance/models/debt.py

- L7: class Debt(models.Model):

- L10: name = models.CharField(max_length=150)

- L11: balance = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L12: minimum_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])

- L13: interest_rate = models.DecimalField(max_digits=8, decimal_places=4, default=0, validators=[MinValueValidator(0)])

- L14: currency = models.CharField(max_length=10, default="USD")

- L15: due_date = models.DateField(null=True, blank=True)

- L16: status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

- L18: class Meta:

- L19: indexes = [models.Index(fields=["user", "status", "due_date"])]

## debt_payment
Source: personal_finance/models/debt_payment.py

- L9: class DebtPayment(models.Model):

- L12: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L13: paid_on = models.DateField()

- L14: note = models.CharField(max_length=255, blank=True)

- L15: transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.SET_NULL, related_name="debt_payment")

- L17: class Meta:

- L19: indexes = [models.Index(fields=["user", "paid_on"])]

## financial_alert
Source: personal_finance/models/financial_alert.py

- L6: class FinancialAlert(models.Model):

- L9: alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

- L10: title = models.CharField(max_length=180)

- L11: message = models.TextField()

- L12: severity = models.CharField(max_length=20, default="info")

- L13: read = models.BooleanField(default=False)

- L14: due_on = models.DateField(null=True, blank=True)

- L15: metadata = models.JSONField(default=dict, blank=True)

- L16: created_at = models.DateTimeField(auto_now_add=True)

- L18: class Meta:

## financial_habit
Source: personal_finance/models/financial_habit.py

- L6: class FinancialHabit(models.Model):

- L9: name = models.CharField(max_length=150)

- L10: target = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L11: duration_days = models.PositiveIntegerField(default=30)

- L12: progress = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L13: streak = models.PositiveIntegerField(default=0)

- L14: started_on = models.DateField()

- L15: status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

- L16: reminder_time = models.TimeField(null=True, blank=True)

## financial_profile
Source: personal_finance/models/financial_profile.py

- L7: class FinancialProfile(models.Model):

- L8: user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_profile")

- L9: base_currency = models.CharField(max_length=10, default="USD")

- L10: emergency_target_months = models.DecimalField(max_digits=5, decimal_places=2, default=3, validators=[MinValueValidator(0)])

- L11: weekly_summary_enabled = models.BooleanField(default=True)

- L12: monthly_summary_enabled = models.BooleanField(default=True)

## financial_scenario
Source: personal_finance/models/financial_scenario.py

- L6: class FinancialScenario(models.Model):

- L9: name = models.CharField(max_length=150)

- L10: income_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)

- L11: expense_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)

- L12: debt_payment_extra = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L13: case = models.CharField(max_length=20, choices=CASE_CHOICES, default="expected")

- L14: result = models.JSONField(default=dict, blank=True)

- L15: created_at = models.DateTimeField(auto_now_add=True)

- L17: class Meta:

## lending_borrowing
Source: personal_finance/models/lending_borrowing.py

- L7: class LendingBorrowing(models.Model):

- L11: direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)

- L12: person = models.CharField(max_length=150)

- L13: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L14: remaining = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L15: currency = models.CharField(max_length=10, default="USD")

- L16: date = models.DateField()

- L17: due_date = models.DateField(null=True, blank=True)

- L18: notes = models.CharField(max_length=500, blank=True)

- L19: status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")

- L21: class Meta:

- L23: indexes = [models.Index(fields=["user", "direction", "status", "due_date"])]

## loan_payment
Source: personal_finance/models/loan_payment.py

- L8: class LoanPayment(models.Model):

- L11: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L12: paid_on = models.DateField()

- L13: note = models.CharField(max_length=255, blank=True)

- L15: class Meta:

## recurring_cashflow
Source: personal_finance/models/recurring_cashflow.py

- L7: class RecurringCashflow(models.Model):

- L11: name = models.CharField(max_length=150)

- L12: kind = models.CharField(max_length=20, choices=KIND_CHOICES)

- L13: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L14: currency = models.CharField(max_length=10, default="USD")

- L15: frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="monthly")

- L16: source = models.CharField(max_length=150, blank=True)

- L17: next_date = models.DateField()

- L18: active = models.BooleanField(default=True)

- L19: description = models.CharField(max_length=255, blank=True)

## savings_goal
Source: personal_finance/models/savings_goal.py

- L7: class SavingsGoal(models.Model):

- L11: name = models.CharField(max_length=150)

- L12: target_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L13: current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])

- L14: currency = models.CharField(max_length=10, default="USD")

- L15: target_date = models.DateField(null=True, blank=True)

- L16: status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

- L18: class Meta:

- L19: indexes = [models.Index(fields=["user", "status", "target_date"])]

## saving_plan
Source: personal_finance/models/saving_plan.py

- L7: class SavingPlan(models.Model):

- L8: goal = models.OneToOneField(SavingsGoal, on_delete=models.CASCADE, related_name="plan")

- L10: daily_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L11: weekly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L12: monthly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

- L13: expected_completion = models.DateField(null=True, blank=True)

## subscription
Source: personal_finance/models/subscription.py

- L7: class Subscription(models.Model):

- L10: name = models.CharField(max_length=150)

- L11: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L12: currency = models.CharField(max_length=10, default="USD")

- L13: billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default="monthly")

- L14: next_charge = models.DateField(null=True, blank=True)

- L15: active = models.BooleanField(default=True)

## transaction
Source: personal_finance/models/transaction.py

- L8: class Transaction(models.Model):

- L17: kind = models.CharField(max_length=20, choices=KIND_CHOICES)

- L18: amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

- L19: currency = models.CharField(max_length=10, default="USD")

- L20: occurred_on = models.DateField()

- L21: description = models.CharField(max_length=255, blank=True)

- L22: payment_method = models.CharField(max_length=50, blank=True)

- L23: priority = models.CharField(max_length=20, default="normal")

- L24: necessity = models.CharField(max_length=20, default="necessary")

- L25: metadata = models.JSONField(default=dict, blank=True)

- L26: created_at = models.DateTimeField(auto_now_add=True)

- L28: class Meta:

- L30: indexes = [

- L31: models.Index(fields=["user", "occurred_on", "kind"]),

- L32: models.Index(fields=["user", "currency", "occurred_on"]),

## __init__
Source: personal_finance/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
