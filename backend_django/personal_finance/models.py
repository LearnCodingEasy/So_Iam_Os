from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    KIND_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
        ("saving", "Saving"),
        ("debt_payment", "Debt payment"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_categories")
    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="expense")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "kind"], name="finance_category_unique"),
        ]
        ordering = ["kind", "name"]


class Transaction(models.Model):
    KIND_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
        ("debt_payment", "Debt payment"),
        ("saving", "Saving"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_transactions")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="transactions")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    occurred_on = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    priority = models.CharField(max_length=20, default="normal")
    necessity = models.CharField(max_length=20, default="necessary")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_on", "-id"]
        indexes = [
            models.Index(fields=["user", "occurred_on", "kind"]),
            models.Index(fields=["user", "currency", "occurred_on"]),
        ]


class Budget(models.Model):
    PERIOD_CHOICES = (("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_budgets")
    name = models.CharField(max_length=150)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="monthly")
    limit_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)


class Debt(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("paid", "Paid"), ("paused", "Paused"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_debts")
    name = models.CharField(max_length=150)
    balance = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    interest_rate = models.DecimalField(max_digits=8, decimal_places=4, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [models.Index(fields=["user", "status", "due_date"])]


class DebtPayment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_debt_payments")
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    paid_on = models.DateField()
    note = models.CharField(max_length=255, blank=True)
    transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.SET_NULL, related_name="debt_payment")

    class Meta:
        ordering = ["-paid_on", "-id"]
        indexes = [models.Index(fields=["user", "paid_on"])]


class LendingBorrowing(models.Model):
    DIRECTION_CHOICES = (("lent", "Lent"), ("borrowed", "Borrowed"))
    STATUS_CHOICES = (("upcoming", "Upcoming"), ("partial", "Partial"), ("paid", "Paid"), ("overdue", "Overdue"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_loans")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    person = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    remaining = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")

    class Meta:
        ordering = ["due_date", "-id"]
        indexes = [models.Index(fields=["user", "direction", "status", "due_date"])]


class LoanPayment(models.Model):
    loan = models.ForeignKey(LendingBorrowing, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_loan_payments")
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    paid_on = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-paid_on", "-id"]


class SavingsGoal(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("completed", "Completed"), ("paused", "Paused"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_savings_goals")
    general_goal = models.ForeignKey("goals.Goal", null=True, blank=True, on_delete=models.SET_NULL, related_name="finance_savings_goals")
    name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [models.Index(fields=["user", "status", "target_date"])]


class SavingPlan(models.Model):
    goal = models.OneToOneField(SavingsGoal, on_delete=models.CASCADE, related_name="plan")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_saving_plans")
    daily_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    weekly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monthly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    expected_completion = models.DateField(null=True, blank=True)


class Subscription(models.Model):
    CYCLE_CHOICES = (("weekly", "Weekly"), ("monthly", "Monthly"), ("quarterly", "Quarterly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_subscriptions")
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default="monthly")
    next_charge = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)


class RecurringCashflow(models.Model):
    KIND_CHOICES = (("income", "Income"), ("expense", "Expense"))
    FREQUENCY_CHOICES = (("daily", "Daily"), ("weekly", "Weekly"), ("biweekly", "Bi-weekly"), ("semimonthly", "Semi-monthly"), ("monthly", "Monthly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_recurring_cashflows")
    name = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="monthly")
    source = models.CharField(max_length=150, blank=True)
    next_date = models.DateField()
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)


class FinancialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_profile")
    base_currency = models.CharField(max_length=10, default="USD")
    emergency_target_months = models.DecimalField(max_digits=5, decimal_places=2, default=3, validators=[MinValueValidator(0)])
    weekly_summary_enabled = models.BooleanField(default=True)
    monthly_summary_enabled = models.BooleanField(default=True)


class FinancialHabit(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("paused", "Paused"), ("completed", "Completed"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_habits")
    name = models.CharField(max_length=150)
    target = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    duration_days = models.PositiveIntegerField(default=30)
    progress = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    streak = models.PositiveIntegerField(default=0)
    started_on = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    reminder_time = models.TimeField(null=True, blank=True)


class FinancialAlert(models.Model):
    TYPE_CHOICES = (("budget", "Budget"), ("spending", "Spending"), ("debt", "Debt"), ("bill", "Bill"), ("goal", "Goal"), ("balance", "Balance"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_alerts")
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=180)
    message = models.TextField()
    severity = models.CharField(max_length=20, default="info")
    read = models.BooleanField(default=False)
    due_on = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["read", "-created_at"]


class FinancialScenario(models.Model):
    CASE_CHOICES = (("best", "Best case"), ("expected", "Expected case"), ("worst", "Worst case"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_scenarios")
    name = models.CharField(max_length=150)
    income_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    expense_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    debt_payment_extra = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    case = models.CharField(max_length=20, choices=CASE_CHOICES, default="expected")
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
