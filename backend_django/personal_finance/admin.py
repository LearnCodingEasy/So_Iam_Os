from django.contrib import admin
from .models import (
    Category, Transaction, Budget, Debt, DebtPayment, LendingBorrowing, LoanPayment,
    SavingsGoal, SavingPlan, Subscription, RecurringCashflow, FinancialProfile,
    FinancialHabit, FinancialAlert, FinancialScenario,
)

for model in (
    Category, Transaction, Budget, Debt, DebtPayment, LendingBorrowing, LoanPayment,
    SavingsGoal, SavingPlan, Subscription, RecurringCashflow, FinancialProfile,
    FinancialHabit, FinancialAlert, FinancialScenario,
):
    admin.site.register(model)
