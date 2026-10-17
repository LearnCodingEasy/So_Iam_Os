from rest_framework import serializers
from .models import (
    Category, Transaction, Budget, Debt, DebtPayment, LendingBorrowing, LoanPayment,
    SavingsGoal, SavingPlan, Subscription, RecurringCashflow, FinancialProfile,
    FinancialHabit, FinancialAlert, FinancialScenario,
)


class OwnedModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def validate_category(self, category):
        if category is not None and category.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Category does not belong to the current user.")
        return category


class CategorySerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Category


class TransactionSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Transaction
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        category = attrs.get("category")
        if category and category.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"category": "Category does not belong to the current user."})
        return attrs


class BudgetSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Budget

    def validate(self, attrs):
        category = attrs.get("category")
        if category and category.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"category": "Category does not belong to the current user."})
        return attrs


class DebtSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Debt


class DebtPaymentSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = DebtPayment
        read_only_fields = ["user"]

    def validate(self, attrs):
        request = self.context["request"]
        debt = attrs.get("debt")
        transaction = attrs.get("transaction")
        if debt and debt.user_id != request.user.id:
            raise serializers.ValidationError({"debt": "Debt does not belong to the current user."})
        if transaction and transaction.user_id != request.user.id:
            raise serializers.ValidationError({"transaction": "Transaction does not belong to the current user."})
        return attrs


class LendingBorrowingSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = LendingBorrowing
        read_only_fields = ["user"]


class LoanPaymentSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = LoanPayment
        read_only_fields = ["user"]

    def validate(self, attrs):
        loan = attrs.get("loan")
        if loan and loan.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"loan": "Loan does not belong to the current user."})
        return attrs


class SavingsGoalSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = SavingsGoal

    def validate(self, attrs):
        goal = attrs.get("general_goal")
        if goal and goal.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"general_goal": "Goal does not belong to the current user."})
        return attrs


class SavingPlanSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = SavingPlan
        read_only_fields = ["user"]

    def validate(self, attrs):
        goal = attrs.get("goal")
        if goal and goal.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"goal": "Goal does not belong to the current user."})
        return attrs


class SubscriptionSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Subscription


class RecurringCashflowSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = RecurringCashflow


class FinancialProfileSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialProfile
        read_only_fields = ["user"]


class FinancialHabitSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialHabit


class FinancialAlertSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialAlert
        read_only_fields = ["user", "created_at"]


class FinancialScenarioSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialScenario
        read_only_fields = ["user", "created_at", "result"]
