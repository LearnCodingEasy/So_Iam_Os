from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum
from django.db import transaction
from ..models import AIBudgetReservation
from django.utils import timezone
from ..models import AIBudgetPolicy, AIUsageRecord

class BudgetService:
    @staticmethod
    def policy(user, scope="user", scope_key=""):
        return AIBudgetPolicy.objects.filter(user=user, scope=scope, scope_key=scope_key, enabled=True).first()

    @classmethod
    def check(cls, *, user, provider="", agent=""):
        policies=[cls.policy(user,"user",""), cls.policy(user,"provider",provider), cls.policy(user,"agent",agent)]
        policies=[p for p in policies if p]
        now=timezone.now()
        day_start=now.replace(hour=0,minute=0,second=0,microsecond=0)
        month_start=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        for p in policies:
            qs=AIUsageRecord.objects.filter(user=user,recorded_at__gte=day_start)
            if p.scope=="provider": qs=qs.filter(provider=p.scope_key)
            if p.scope=="agent": qs=qs.filter(agent=p.scope_key)
            daily_cost=qs.aggregate(v=Sum("estimated_cost"))["v"] or Decimal("0")
            daily_tokens=(qs.aggregate(v=Sum("input_tokens"))["v"] or 0)+(qs.aggregate(v=Sum("output_tokens"))["v"] or 0)
            qs2=AIUsageRecord.objects.filter(user=user,recorded_at__gte=month_start)
            if p.scope=="provider": qs2=qs2.filter(provider=p.scope_key)
            if p.scope=="agent": qs2=qs2.filter(agent=p.scope_key)
            monthly_cost=qs2.aggregate(v=Sum("estimated_cost"))["v"] or Decimal("0")
            monthly_tokens=(qs2.aggregate(v=Sum("input_tokens"))["v"] or 0)+(qs2.aggregate(v=Sum("output_tokens"))["v"] or 0)
            if p.daily_cost_limit is not None and daily_cost >= p.daily_cost_limit: return False, "daily_cost_limit"
            if p.monthly_cost_limit is not None and monthly_cost >= p.monthly_cost_limit: return False, "monthly_cost_limit"
            if p.daily_token_limit is not None and daily_tokens >= p.daily_token_limit: return False, "daily_token_limit"
            if p.monthly_token_limit is not None and monthly_tokens >= p.monthly_token_limit: return False, "monthly_token_limit"
        return True, None


    @classmethod
    @transaction.atomic
    def reserve(cls, *, user, estimated_cost=Decimal("0"), estimated_tokens=0,
                idempotency_key="", provider="", agent="", ttl_seconds=300):
        if not idempotency_key:
            raise ValueError("idempotency_key is required for budget reservations.")
        existing = AIBudgetReservation.objects.select_for_update().filter(
            user=user, idempotency_key=idempotency_key).first()
        if existing:
            return existing
        policies = [cls.policy(user, "user", ""), cls.policy(user, "provider", provider), cls.policy(user, "agent", agent)]
        policies = [p for p in policies if p]
        policy = policies[0] if policies else None
        if policy is None:
            return None
        ok, reason = cls.check(user=user, provider=provider, agent=agent)
        if not ok:
            raise ValueError(f"AI budget exceeded: {reason}")
        estimated_cost = max(Decimal("0"), Decimal(str(estimated_cost)))
        estimated_tokens = max(0, int(estimated_tokens))
        now = timezone.now()
        if policy.daily_cost_limit is not None:
            used = AIUsageRecord.objects.filter(user=user, recorded_at__gte=now.replace(hour=0, minute=0, second=0, microsecond=0)).aggregate(v=Sum("estimated_cost"))["v"] or Decimal("0")
            reserved = AIBudgetReservation.objects.filter(user=user, policy=policy, status="reserved", expires_at__gt=now).aggregate(v=Sum("reserved_cost"))["v"] or Decimal("0")
            if used + reserved + estimated_cost > policy.daily_cost_limit:
                raise ValueError("AI budget reservation exceeds the daily cost limit.")
        return AIBudgetReservation.objects.create(
            user=user, policy=policy, idempotency_key=idempotency_key,
            reserved_cost=estimated_cost, reserved_tokens=estimated_tokens,
            expires_at=now + timedelta(seconds=max(30, int(ttl_seconds))),
        )

    @classmethod
    @transaction.atomic
    def settle(cls, reservation, *, actual_cost=None, actual_tokens=None):
        reservation = AIBudgetReservation.objects.select_for_update().get(pk=reservation.pk)
        if reservation.status != "reserved":
            return reservation
        reservation.reserved_cost = max(Decimal("0"), Decimal(str(actual_cost if actual_cost is not None else reservation.reserved_cost)))
        if actual_tokens is not None:
            reservation.reserved_tokens = max(0, int(actual_tokens))
        reservation.status = "settled"
        reservation.save(update_fields=["reserved_cost", "reserved_tokens", "status", "updated_at"])
        return reservation

    @classmethod
    @transaction.atomic
    def release(cls, reservation):
        reservation = AIBudgetReservation.objects.select_for_update().get(pk=reservation.pk)
        if reservation.status == "reserved":
            reservation.status = "released"
            reservation.save(update_fields=["status", "updated_at"])
        return reservation
