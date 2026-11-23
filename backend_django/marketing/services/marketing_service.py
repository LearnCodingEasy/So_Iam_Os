"""Campaign performance and lead attribution."""
from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Count, Sum
from django.utils import timezone

from crm.models import Contact
from marketing.models import Campaign, MarketingContent

CENT = Decimal("0.01")


def _money(value):
    return str(Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP))


def mark_published(content):
    if content.status != MarketingContent.STATUS_PUBLISHED:
        content.status = MarketingContent.STATUS_PUBLISHED
        content.published_at = timezone.now()
        content.save(update_fields=["status", "published_at", "updated_at"])
    return content


def campaign_leads(campaign):
    """Distinct CRM contacts attributed to the campaign through its lead sources."""
    return Contact.objects.filter(lead_sources__campaign=campaign, user=campaign.user).distinct().count()


def campaign_performance(campaign):
    leads = campaign_leads(campaign)
    contents = dict(campaign.contents.values_list("status").annotate(n=Count("id")))
    return {
        "campaign": campaign.pk,
        "status": campaign.status,
        "budget": _money(campaign.budget),
        "spent": _money(campaign.spent),
        "remaining": _money(campaign.budget - campaign.spent),
        "over_budget": campaign.spent > campaign.budget,
        "leads": leads,
        "cost_per_lead": _money(campaign.spent / leads) if leads else None,
        "content": {"total": sum(contents.values()), "by_status": contents},
    }


def overview(user):
    campaigns = Campaign.objects.filter(user=user)
    totals = campaigns.aggregate(budget=Sum("budget"), spent=Sum("spent"))
    by_status = dict(campaigns.values_list("status").annotate(n=Count("id")))
    leads = Contact.objects.filter(user=user, lead_sources__isnull=False).distinct().count()
    spent = totals["spent"] or Decimal("0")
    return {
        "campaigns": sum(by_status.values()),
        "by_status": by_status,
        "budget": _money(totals["budget"] or 0),
        "spent": _money(spent),
        "leads": leads,
        "cost_per_lead": _money(spent / leads) if leads else None,
        "published_content": MarketingContent.objects.filter(user=user, status=MarketingContent.STATUS_PUBLISHED).count(),
    }
