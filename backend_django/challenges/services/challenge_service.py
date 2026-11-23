"""Challenge progress and attempt business logic."""
from django.db import transaction

from challenges.models import ChallengeAttempt, ChallengeProgress

PASS_SCORE = 70


def percent_for(completed_steps, total_steps):
    if total_steps <= 0:
        return 0
    return min(100, round(completed_steps * 100 / total_steps))


@transaction.atomic
def set_progress(*, user, challenge, completed_steps=None, progress_percent=None):
    """Create or update the single progress row of ``user`` for ``challenge``.

    When ``completed_steps`` is given and the challenge has steps, the percentage
    is derived from it; otherwise ``progress_percent`` is stored as given.
    """
    total = challenge.steps.count()
    row, _ = ChallengeProgress.objects.select_for_update().get_or_create(challenge=challenge, user=user)
    if completed_steps is not None:
        row.completed_steps = min(completed_steps, total) if total else completed_steps
        if total:
            row.progress_percent = percent_for(row.completed_steps, total)
    if progress_percent is not None and (completed_steps is None or not total):
        row.progress_percent = progress_percent
    row.save()
    return row


@transaction.atomic
def complete_step(*, user, challenge):
    """Advance the user's completed step count by one (never above the step total)."""
    total = challenge.steps.count()
    row, _ = ChallengeProgress.objects.select_for_update().get_or_create(challenge=challenge, user=user)
    if total and row.completed_steps >= total:
        return row
    row.completed_steps += 1
    if total:
        row.completed_steps = min(row.completed_steps, total)
        row.progress_percent = percent_for(row.completed_steps, total)
    row.save()
    return row


@transaction.atomic
def record_attempt(*, user, challenge, **data):
    """Store an attempt; a passing score completes the user's progress."""
    attempt = ChallengeAttempt.objects.create(user=user, challenge=challenge, **data)
    if attempt.score >= PASS_SCORE:
        total = challenge.steps.count()
        row, _ = ChallengeProgress.objects.select_for_update().get_or_create(challenge=challenge, user=user)
        row.progress_percent = 100
        row.completed_steps = total or row.completed_steps
        row.save()
    return attempt
