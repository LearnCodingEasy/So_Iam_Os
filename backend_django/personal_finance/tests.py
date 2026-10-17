from datetime import date, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase

from users_accounts.models import User
from .models import Category, Debt, SavingsGoal, Transaction


class FinanceAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="finance-a@example.com", password="StrongPass123!")
        self.other = User.objects.create_user(email="finance-b@example.com", password="StrongPass123!")
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(user=self.user, name="Food", kind="expense")
        self.other_category = Category.objects.create(user=self.other, name="Private", kind="expense")
        Transaction.objects.create(user=self.user, category=self.category, kind="income", amount=Decimal("5000"), currency="EGP", occurred_on=date.today())
        Transaction.objects.create(user=self.user, category=self.category, kind="expense", amount=Decimal("1000"), currency="EGP", occurred_on=date.today())
        Debt.objects.create(user=self.user, name="Card", balance=Decimal("2000"), minimum_payment=Decimal("200"), currency="EGP")
        SavingsGoal.objects.create(user=self.user, name="Laptop", target_amount=Decimal("5000"), current_amount=Decimal("1000"), currency="EGP", target_date=date.today()+timedelta(days=90))

    def test_dashboard_is_user_scoped(self):
        response = self.client.get("/api/finance/transactions/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["income"], Decimal("5000"))
        self.assertEqual(response.data["expenses"], Decimal("1000"))

    def test_foreign_category_is_rejected(self):
        response = self.client.post("/api/finance/transactions/", {
            "category": self.other_category.id, "kind": "expense", "amount": "10",
            "currency": "EGP", "occurred_on": str(date.today()), "description": "attack",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.data)

    def test_health_forecast_reports_and_contract(self):
        for path in (
            "/api/finance/health/",
            "/api/finance/forecast/",
            "/api/finance/daily-summary/",
            "/api/finance/reports/weekly/",
            "/api/finance/reports/monthly/",
            "/api/finance/contract/",
        ):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_debt_payment_reduces_balance_and_creates_transaction(self):
        debt = self.user.finance_debts.get(name="Card")
        response = self.client.post(f"/api/finance/debts/{debt.id}/pay/", {"amount": "500", "paid_on": str(date.today())}, format="json")
        self.assertEqual(response.status_code, 201)
        debt.refresh_from_db()
        self.assertEqual(debt.balance, Decimal("1500"))
        self.assertTrue(Transaction.objects.filter(user=self.user, kind="debt_payment", amount=Decimal("500")).exists())

    def test_user_cannot_see_other_users_data(self):
        Transaction.objects.create(user=self.other, kind="expense", amount=Decimal("99999"), currency="EGP", occurred_on=date.today())
        response = self.client.get("/api/finance/transactions/")
        self.assertEqual(response.status_code, 200)
        rows = response.data["results"] if isinstance(response.data, dict) and "results" in response.data else response.data
        self.assertTrue(all(row["amount"] != "99999.00" for row in rows))
