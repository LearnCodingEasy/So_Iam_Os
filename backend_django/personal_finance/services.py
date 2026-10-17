from __future__ import annotations

from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone

from .models import (
    Budget, Debt, DebtPayment, FinancialAlert, FinancialProfile, FinancialScenario,
    FinancialHabit, LendingBorrowing, LoanPayment, RecurringCashflow, SavingsGoal,
    Subscription, Transaction,
)

ZERO = Decimal("0")


def profile_for(user):
    profile, _ = FinancialProfile.objects.get_or_create(user=user)
    return profile


def _money(value):
    return Decimal(value or 0)


def _range_for_period(today, period="month"):
    if period == "day":
        return today, today
    if period == "week":
        start = today - timedelta(days=today.weekday())
        return start, today
    if period == "year":
        return today.replace(month=1, day=1), today
    return today.replace(day=1), today


def _totals(qs):
    return {
        "income": _money(qs.filter(kind="income").aggregate(v=Sum("amount"))["v"]),
        "expenses": _money(qs.filter(kind="expense").aggregate(v=Sum("amount"))["v"]),
        "savings": _money(qs.filter(kind="saving").aggregate(v=Sum("amount"))["v"]),
        "debt_payments": _money(qs.filter(kind="debt_payment").aggregate(v=Sum("amount"))["v"]),
    }


def dashboard(user, start=None, end=None):
    today = timezone.localdate()
    start = start or today.replace(day=1)
    end = end or today
    qs = Transaction.objects.filter(
        user=user, occurred_on__gte=start, occurred_on__lte=end)
    totals = _totals(qs)
    balance = totals["income"] - totals["expenses"] - \
        totals["savings"] - totals["debt_payments"]
    upcoming_bills = list(
        Subscription.objects.filter(
            user=user, active=True, next_charge__gte=today, next_charge__lte=today + timedelta(days=30)
        ).values("id", "name", "amount", "currency", "next_charge")[:20]
    )
    debts = list(
        Debt.objects.filter(user=user, status="active")
        .values("id", "name", "balance", "minimum_payment", "interest_rate", "currency", "due_date")[:20]
    )
    goals = list(
        SavingsGoal.objects.filter(user=user, status="active")
        .values("id", "name", "target_amount", "current_amount", "currency", "target_date")[:20]
    )
    budget_rows = []
    for budget in Budget.objects.filter(user=user, active=True).select_related("category"):
        if budget.category_id:
            spent = qs.filter(kind="expense", category=budget.category).aggregate(
                v=Sum("amount"))["v"] or ZERO
        else:
            spent = qs.filter(kind="expense", currency=budget.currency).aggregate(
                v=Sum("amount"))["v"] or ZERO
        budget_rows.append({
            "id": budget.id, "name": budget.name, "period": budget.period,
            "limit": budget.limit_amount, "spent": spent,
            "remaining": _money(budget.limit_amount) - _money(spent), "currency": budget.currency,
        })
    return {
        "period": {"from": start, "to": end},
        **totals,
        "balance": balance,
        "upcoming_bills": upcoming_bills,
        "debts": debts,
        "goals": goals,
        "budgets": budget_rows,
        "base_currency": profile_for(user).base_currency,
    }


def summary(user):
    data = dashboard(user)
    return {k: data[k] for k in ("income", "expenses", "savings", "debt_payments", "balance")}


def spending_breakdown(user, start=None, end=None):
    data = dashboard(user, start, end)
    qs = Transaction.objects.filter(
        user=user, kind="expense", occurred_on__gte=data["period"]["from"], occurred_on__lte=data["period"]["to"])
    rows = list(qs.values("currency").annotate(
        total=Sum("amount")).order_by("-total"))
    categories = list(
        qs.values("category", "category__name", "currency").annotate(
            total=Sum("amount")).order_by("-total")[:20]
    )
    return {"period": data["period"], "by_currency": rows, "by_category": categories}


def financial_health(user):
    today = timezone.localdate()
    current = dashboard(user)
    prev_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    prev_end = today.replace(day=1) - timedelta(days=1)
    previous = dashboard(user, prev_start, prev_end)
    income = _money(current["income"])
    expenses = _money(current["expenses"])
    savings = _money(current["savings"])
    debt_total = _money(Debt.objects.filter(
        user=user, status="active").aggregate(v=Sum("balance"))["v"])
    savings_rate = (savings / income * 100) if income > 0 else ZERO
    expense_ratio = (expenses / income * 100) if income > 0 else ZERO
    debt_load = (debt_total / income * 100) if income > 0 else ZERO
    recurring = _money(
        Subscription.objects.filter(
            user=user, active=True).aggregate(v=Sum("amount"))["v"]
    )
    emergency_months = (
        current["balance"] / expenses) if expenses > 0 and current["balance"] > 0 else ZERO
    budget_ok = sum(1 for b in current["budgets"]
                    if _money(b["remaining"]) >= 0)
    budget_total = len(current["budgets"])
    budget_adherence = (Decimal(budget_ok) / Decimal(budget_total)
                        * 100) if budget_total else Decimal("100")
    income_stability = Decimal("100") if previous["income"] and income >= previous["income"] * Decimal(
        "0.8") else Decimal("60") if income else Decimal("0")
    components = {
        "spending_control": max(0, min(100, Decimal("100") - max(0, expense_ratio - 60))),
        "savings": max(0, min(100, savings_rate * 2)),
        "debt_management": max(0, min(100, Decimal("100") - debt_load)),
        "goal_progress": _goal_progress(user),
        "budget_adherence": budget_adherence,
        "income_stability": income_stability,
    }
    score = sum(components.values()) / Decimal(len(components))
    return {
        "score": score.quantize(Decimal("0.01")),
        "label": "excellent" if score >= 80 else "good" if score >= 65 else "attention" if score >= 45 else "critical",
        "metrics": {
            "income_stability": income_stability.quantize(Decimal("0.01")),
            "expense_ratio": expense_ratio.quantize(Decimal("0.01")),
            "savings_rate": savings_rate.quantize(Decimal("0.01")),
            "debt_load": debt_load.quantize(Decimal("0.01")),
            "recurring_expenses": recurring,
            "emergency_buffer_months": emergency_months.quantize(Decimal("0.01")),
            "goal_progress": components["goal_progress"].quantize(Decimal("0.01")),
            "budget_adherence": budget_adherence.quantize(Decimal("0.01")),
        },
        "components": {
            k: (Decimal(str(v)).quantize(Decimal("0.01"))
                if v is not None else Decimal("0.00"))
            for k, v in components.items()
        },
        "explanation": [
            "النتيجة مؤشر تخطيطي قابل للتفسير وليست حكماً مالياً.",
            "تحسين الادخار، خفض المصروفات المتكررة، وسداد الديون في موعدها يرفع المؤشر.",
        ],
    }


def _goal_progress(user):
    goals = SavingsGoal.objects.filter(user=user, status="active")
    if not goals.exists():
        return Decimal("0")
    values = []
    for goal in goals:
        target = _money(goal.target_amount)
        values.append(min(Decimal("100"), _money(
            goal.current_amount) / target * 100) if target else Decimal("0"))
    return sum(values) / Decimal(len(values))


def forecast(user, months=3):
    today = timezone.localdate()
    start = today - timedelta(days=90)
    qs = Transaction.objects.filter(
        user=user, occurred_on__gte=start, occurred_on__lte=today)
    totals = _totals(qs)
    avg_month_income = totals["income"] / Decimal("3")
    avg_month_expenses = totals["expenses"] / Decimal("3")
    avg_month_savings = totals["savings"] / Decimal("3")
    recurring_income = _money(RecurringCashflow.objects.filter(
        user=user, kind="income", active=True).aggregate(v=Sum("amount"))["v"])
    recurring_expenses = _money(RecurringCashflow.objects.filter(
        user=user, kind="expense", active=True).aggregate(v=Sum("amount"))["v"])
    base_income = avg_month_income if avg_month_income > 0 else recurring_income
    base_expenses = avg_month_expenses if avg_month_expenses > 0 else recurring_expenses
    rows = []
    running = ZERO
    for offset in range(max(1, min(int(months), 24))):
        month_date = (today.replace(day=1) +
                      timedelta(days=32 * offset)).replace(day=1)
        income = base_income + recurring_income
        expenses = base_expenses + recurring_expenses
        surplus = income - expenses
        running += surplus
        rows.append({"month": month_date, "income": income, "expenses": expenses, "savings": max(
            ZERO, surplus), "surplus": surplus, "cumulative_surplus": running})
    return {
        "assumptions": {"history_days": 90, "months": len(rows), "base_currency": profile_for(user).base_currency},
        "history": totals,
        "forecast": rows,
        "goal_progress": _goal_projection(user, running),
    }


def _goal_projection(user, surplus):
    result = []
    for goal in SavingsGoal.objects.filter(user=user, status="active"):
        remaining = max(ZERO, _money(goal.target_amount) -
                        _money(goal.current_amount))
        monthly = max(ZERO, surplus)
        months = (remaining / monthly) if monthly else None
        result.append({"id": goal.id, "name": goal.name,
                      "remaining": remaining, "estimated_months": months})
    return result


def scenario(user, income_change=0, expense_change=0, extra_debt_payment=0, case="expected"):
    base = forecast(user, 1)["forecast"][0]
    income = _money(base["income"]) * (Decimal("1") +
                                       Decimal(str(income_change)) / 100)
    expenses = _money(base["expenses"]) * \
        (Decimal("1") + Decimal(str(expense_change)) / 100)
    surplus = income - expenses - _money(extra_debt_payment)
    return {
        "case": case,
        "income": income,
        "expenses": expenses,
        "extra_debt_payment": _money(extra_debt_payment),
        "surplus": surplus,
        "impact": "surplus" if surplus >= 0 else "shortage",
    }


def alerts_for_user(user):
    today = timezone.localdate()
    data = dashboard(user)
    alerts = []
    for budget in data["budgets"]:
        if budget["remaining"] < 0:
            alerts.append(
                ("budget", f"تجاوز ميزانية {budget['name']}", "المصروف الحالي تجاوز الحد المحدد.", "warning"))
    for debt in data["debts"]:
        if debt["due_date"] and debt["due_date"] <= today + timedelta(days=7):
            alerts.append(
                ("debt", f"استحقاق دين قريب: {debt['name']}", "راجع الدفعة القادمة.", "warning"))
    for bill in data["upcoming_bills"]:
        if bill["next_charge"] <= today + timedelta(days=7):
            alerts.append(
                ("bill", f"فاتورة قريبة: {bill['name']}", "هناك التزام متكرر خلال 7 أيام.", "info"))
    if data["income"] and data["expenses"] > data["income"]:
        alerts.append(("balance", "المصروفات أعلى من الدخل",
                      "راجع المصروفات المتغيرة والالتزامات القادمة.", "danger"))
    for alert_type, title, message, severity in alerts:
        FinancialAlert.objects.get_or_create(
            user=user, alert_type=alert_type, title=title, read=False,
            defaults={"message": message, "severity": severity},
        )
    return FinancialAlert.objects.filter(user=user, read=False)


def insights(user):
    data = dashboard(user)
    health = financial_health(user)
    tips = []
    if data["income"] and data["expenses"] > data["income"]:
        tips.append({"type": "warning", "title": "المصروفات أعلى من الدخل",
                    "detail": "راجع المصروفات المتغيرة والالتزامات قبل إضافة التزامات جديدة."})
    elif data["income"]:
        rate = (data["income"] - data["expenses"]) / data["income"] * 100
        tips.append({"type": "info", "title": "فائض شهري تقديري",
                    "detail": f"يتبقى حوالي {rate:.0f}% من الدخل بعد المصروفات المسجلة."})
    if health["metrics"]["savings_rate"] < 10:
        tips.append({"type": "saving", "title": "ارفع معدل الادخار تدريجيًا",
                    "detail": "ابدأ بهدف صغير ثابت بدل الاعتماد على مبلغ كبير غير منتظم."})
    for budget in data["budgets"]:
        if budget["remaining"] < 0:
            tips.append(
                {"type": "warning", "title": f"تجاوز الميزانية: {budget['name']}", "detail": "قلل المصروف الاختياري أو أعد ضبط الميزانية."})
    alerts_for_user(user)
    return {"disclaimer": "مساعدة تخطيطية معلوماتية وليست نصيحة مالية مهنية.", "insights": tips[:10]}


def daily_summary(user):
    today = timezone.localdate()
    return dashboard(user, today, today)


def period_report(user, period="monthly"):
    today = timezone.localdate()
    if period == "weekly":
        start, end = _range_for_period(today, "week")
    else:
        start, end = _range_for_period(today, "month")
    data = dashboard(user, start, end)
    previous_end = start - timedelta(days=1)
    previous_start = previous_end - (end - start)
    previous = dashboard(user, previous_start, previous_end)
    return {
        "period": data["period"],
        "current": {k: data[k] for k in ("income", "expenses", "savings", "debt_payments", "balance")},
        "previous": {k: previous[k] for k in ("income", "expenses", "savings", "debt_payments", "balance")},
        "changes": {
            k: (_money(data[k]) - _money(previous[k])) for k in ("income", "expenses", "savings", "debt_payments", "balance")
        },
        "insights": insights(user)["insights"],
    }


def coach_answer(user, question):
    data = dashboard(user)
    health = financial_health(user)
    q = (question or "").lower()
    if any(word in q for word in ("laptop", "شراء", "buy")):
        return f"راجع رصيدك الحالي {data['balance']} {health['metrics'].get('base_currency', '')} ومعدل الادخار. الأفضل اختبار الشراء داخل سيناريو قبل اتخاذ القرار."
    if any(word in q for word in ("وفر", "saving", "ادخار")):
        return f"معدل الادخار الحالي حوالي {health['metrics']['savings_rate']}%. ابدأ بهدف أسبوعي صغير وراقب الالتزام."
    return (
        f"الصورة الحالية: دخل {data['income']}، مصروفات {data['expenses']}، "
        f"ادخار {data['savings']}، ونتيجة الصحة المالية {health['score']}/100. "
        "استخدم الأرقام دي كنقطة بداية لخطة عملية، والقرار النهائي لك."
    )


def ecosystem_integration(user):
    result = {
        "finance": {
            "transactions": Transaction.objects.filter(user=user).count(),
            "goals": SavingsGoal.objects.filter(user=user).count(),
            "debts": Debt.objects.filter(user=user, status="active").count(),
        },
        "connections": {},
    }
    checks = [
        ("goals", "goals.models", "Goal"),
        ("tasks", "tasks.models", "Task"),
        ("learning", "learning.models", "LearningGoal"),
        ("jobs", "jobs_opportunity.models", "JobOpportunity"),
        ("projects", "projects.models", "Project"),
        ("memory", "memory.models", "MemoryItem"),
        ("challenges", "challenges.models", "Challenge"),
        ("notifications", "notification.models", "Notification"),
        ("automation", "automation.models", "Workflow"),
    ]
    for key, module_name, class_name in checks:
        try:
            module = __import__(module_name, fromlist=[class_name])
            model = getattr(module, class_name)
            result["connections"][key] = {
                "available": True,
                "count": model.objects.filter(user=user).count(),
            }
        except Exception as exc:
            result["connections"][key] = {"available": False, "count": 0, "reason": str(exc)[
                :120]}
    try:
        from jobs_opportunity.models import JobRecommendation
        result["income_opportunities"] = JobRecommendation.objects.filter(
            user=user).count()
    except Exception:
        result["income_opportunities"] = 0
    result["recommended_flow"] = [
        "Financial Goal → Learning Goal → Skill → Job Opportunity → Potential Income",
        "Financial Event → Task / Notification",
        "Project → Cost / Revenue → Financial Analysis",
        "Approved financial preferences → Memory (only when explicitly appropriate)",
    ]
    return result
