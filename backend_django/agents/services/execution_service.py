"""Agent run lifecycle and execution through the central AI gateway.

State machine::

    awaiting_approval --approve--> pending --execute--> running --> succeeded | failed
    awaiting_approval | pending | running --cancel--> cancelled

``execute_run`` calls ``ai.services.agent_executor.AgentExecutor`` (the same
validated boundary used by the AI app). Nothing is simulated: if no AI provider is
configured for the user the run is marked ``failed`` with the provider error.
"""
import time

from django.db import transaction
from django.utils import timezone

from agents.models import Agent, AgentExecution, AgentRun
from agents.services.agent_service import get_active_configuration


class AgentRunError(Exception):
    """Raised for an operation that is not allowed in the run's current state."""


def _default_executor(user):
    from ai.services.agent_executor import AgentExecutor

    return AgentExecutor(user=user)


def create_run(*, user, agent, goal, input_data=None):
    if agent.user_id != user.pk:
        raise AgentRunError("Agent not found.")
    if agent.status != Agent.STATUS_ACTIVE:
        raise AgentRunError("Only active agents can start runs.")
    status = AgentRun.STATUS_AWAITING_APPROVAL if agent.requires_approval else AgentRun.STATUS_PENDING
    return AgentRun.objects.create(
        user=user,
        agent=agent,
        configuration=get_active_configuration(agent),
        goal=goal,
        input_data=input_data or {},
        status=status,
        approved_at=None if agent.requires_approval else timezone.now(),
    )


@transaction.atomic
def _locked(run):
    return AgentRun.objects.select_for_update().get(pk=run.pk)


def approve_run(run):
    with transaction.atomic():
        run = _locked(run)
        if run.status != AgentRun.STATUS_AWAITING_APPROVAL:
            raise AgentRunError("Only runs awaiting approval can be approved.")
        run.status = AgentRun.STATUS_PENDING
        run.approved_at = timezone.now()
        run.save(update_fields=["status", "approved_at"])
    return run


def cancel_run(run):
    with transaction.atomic():
        run = _locked(run)
        if run.status in AgentRun.TERMINAL_STATUSES:
            raise AgentRunError("A finished run cannot be cancelled.")
        run.status = AgentRun.STATUS_CANCELLED
        run.finished_at = timezone.now()
        run.save(update_fields=["status", "finished_at"])
    return run


def _build_messages(run):
    messages = []
    prompt = (run.agent.system_prompt or "").strip()
    if prompt:
        messages.append({"role": "system", "content": prompt})
    content = run.goal.strip()
    if run.input_data:
        content += "\n\nContext (JSON): %s" % run.input_data
    messages.append({"role": "user", "content": content})
    return messages


def execute_run(run, executor=None):
    """Execute a pending run once and persist the outcome and its step record."""
    with transaction.atomic():
        run = _locked(run)
        if run.status != AgentRun.STATUS_PENDING:
            raise AgentRunError("Only approved, pending runs can be executed.")
        run.status = AgentRun.STATUS_RUNNING
        run.started_at = timezone.now()
        run.save(update_fields=["status", "started_at"])

    configuration = run.configuration
    executor = executor or _default_executor(run.user)
    messages = _build_messages(run)
    step_input = {"messages": len(messages), "model": run.agent.model_name or None}
    began = time.monotonic()
    try:
        result = executor.execute(
            provider=None,
            messages=messages,
            model=run.agent.model_name or None,
            temperature=configuration.temperature if configuration else None,
        )
        output = {"content": str(result.get("content", "")), "provider": result.get("provider"),
                  "model": result.get("model")}
        step_status, error = AgentExecution.STATUS_SUCCEEDED, ""
    except Exception as exc:  # AIError, ValueError or provider failure: report, never fake success
        output, step_status = {}, AgentExecution.STATUS_FAILED
        error = "%s: %s" % (getattr(exc, "category", type(exc).__name__), exc)
    duration = int((time.monotonic() - began) * 1000)

    with transaction.atomic():
        run = _locked(run)
        AgentExecution.objects.create(
            run=run, step_index=1, action="llm_completion", status=step_status,
            input_data=step_input, output_data=output, error=error, duration_ms=duration,
        )
        if run.status == AgentRun.STATUS_CANCELLED:  # cancelled while the provider was busy
            return run
        run.finished_at = timezone.now()
        if step_status == AgentExecution.STATUS_SUCCEEDED:
            run.status, run.result = AgentRun.STATUS_SUCCEEDED, output
        else:
            run.status, run.error = AgentRun.STATUS_FAILED, error
        run.save(update_fields=["status", "result", "error", "finished_at"])
    return run
