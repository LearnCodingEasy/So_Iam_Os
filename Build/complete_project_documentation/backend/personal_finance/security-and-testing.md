# personal_finance security and testing

## Permission/ownership evidence

- personal_finance/api/views/common.py:L2: from rest_framework.decorators import api_view, permission_classes
- personal_finance/api/views/common.py:L3: from rest_framework.permissions import IsAuthenticated
- personal_finance/api/views/common.py:L11: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L13: return Response(financial_health(request.user))
- personal_finance/api/views/common.py:L17: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L20: return Response(forecast(request.user, months))
- personal_finance/api/views/common.py:L24: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L27: request.user,
- personal_finance/api/views/common.py:L34: user=request.user,
- personal_finance/api/views/common.py:L46: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L48: return Response(daily_summary(request.user))
- personal_finance/api/views/common.py:L52: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L56: return Response(period_report(request.user, period))
- personal_finance/api/views/common.py:L60: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L67: "answer": coach_answer(request.user, question),
- personal_finance/api/views/common.py:L72: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L74: alerts_for_user(request.user)
- personal_finance/api/views/common.py:L75: return Response(FinancialAlertSerializer(FinancialAlert.objects.filter(user=request.user, read=False), many=True).data)
- personal_finance/api/views/common.py:L79: @permission_classes([IsAuthenticated])
- personal_finance/api/views/common.py:L81: return Response(ecosystem_integration(request.user))
- personal_finance/api/views/common.py:L85: @permission_classes([IsAuthenticated])
- personal_finance/api/views/debt_views.py:L33: user=request.user, kind="debt_payment", amount=amount, currency=debt.currency,
- personal_finance/api/views/debt_views.py:L36: payment = DebtPayment.objects.create(user=request.user, debt=debt, amount=amount, paid_on=paid_on, note=note, transaction=tx)
- personal_finance/api/views/financial_scenario_views.py:L13: instance = serializer.save(user=self.request.user)
- personal_finance/api/views/financial_scenario_views.py:L15: self.request.user,
- personal_finance/api/views/lending_borrowing_views.py:L24: user=request.user, loan=loan, amount=amount,
- personal_finance/api/views/owned_views.py:L3: from rest_framework.decorators import permission_classes
- personal_finance/api/views/owned_views.py:L4: from rest_framework.permissions import IsAuthenticated
- personal_finance/api/views/owned_views.py:L8: permission_classes = [IsAuthenticated]
- personal_finance/api/views/owned_views.py:L11: serializer.save(user=self.request.user)
- personal_finance/api/views/owned_views.py:L13: def get_queryset(self):
- personal_finance/api/views/owned_views.py:L14: return self.queryset.filter(user=self.request.user)
- personal_finance/api/views/savings_goal_views.py:L30: goal=goal, defaults={"user": request.user, "daily_amount": daily, "weekly_amount": weekly, "monthly_amount": monthly, "expected_completion": goal.target_date}
- personal_finance/api/views/transaction_views.py:L17: return Response(dashboard(request.user))
- personal_finance/api/views/transaction_views.py:L21: return Response(dashboard(request.user))
- personal_finance/api/views/transaction_views.py:L25: return Response(insights(request.user))
- personal_finance/api/views/transaction_views.py:L36: return Response(dashboard(request.user, parsed_start, parsed_end))
- personal_finance/api/views/transaction_views.py:L40: return Response(spending_breakdown(request.user))
- personal_finance/api/views/transaction_views.py:L54: + json.dumps(dashboard(request.user), default=str, ensure_ascii=False)
- personal_finance/api/views/transaction_views.py:L57: result = AIService(request.user).chat(prompt)
- personal_finance/api/views/transaction_views.py:L67: "fallback": insights(request.user),


## Tests
- personal_finance/tests/test_personal_finance.py
- personal_finance/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
