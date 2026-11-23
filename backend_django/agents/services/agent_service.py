"""Agent configuration business logic."""
from django.db import transaction
from django.db.models import Max

from agents.models import Agent, AgentConfiguration


@transaction.atomic
def create_configuration(*, agent, **data):
    """Create the next numbered configuration for ``agent``.

    The agent row is locked so concurrent requests cannot allocate the same
    version number (the DB unique constraint is the last line of defence).
    """
    Agent.objects.select_for_update().get(pk=agent.pk)
    latest = AgentConfiguration.objects.filter(agent=agent).aggregate(m=Max("version"))["m"] or 0
    return AgentConfiguration.objects.create(agent=agent, version=latest + 1, **data)


@transaction.atomic
def activate_configuration(configuration):
    """Make ``configuration`` the only active version of its agent."""
    Agent.objects.select_for_update().get(pk=configuration.agent_id)
    AgentConfiguration.objects.filter(agent_id=configuration.agent_id, is_active=True).exclude(
        pk=configuration.pk
    ).update(is_active=False)
    if not configuration.is_active:
        configuration.is_active = True
        configuration.save(update_fields=["is_active"])
    return configuration


def get_active_configuration(agent):
    return agent.configurations.filter(is_active=True).first()
