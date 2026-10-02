from django.db.models import Q
from .models import Friendship, Follow, UserBlock, SocialProfile, SocialRecommendation


def _norm(values):
    return {str(v).strip().lower() for v in (values or []) if str(v).strip()}


def _user_skills(user):
    result = set()
    for item in user.skills or []:
        if isinstance(item, dict):
            value = item.get("slug") or item.get("name")
        else:
            value = item
        if value:
            result.add(str(value).strip().lower())
    try:
        result.update(user.learning_goals.select_related("skill").filter(skill__isnull=False).values_list("skill__slug", flat=True))
    except Exception:
        pass
    return _norm(result)


def score_candidate(user, candidate):
    source = getattr(user, "social_profile", None)
    target = getattr(candidate, "social_profile", None)
    source = source or SocialProfile(user=user)
    target = target or SocialProfile(user=candidate)
    user_skills, candidate_skills = _user_skills(user), _user_skills(candidate)
    user_interests = _norm(source.learning_interests) | _norm(source.professional_interests) | _norm(source.topics)
    candidate_interests = _norm(target.learning_interests) | _norm(target.professional_interests) | _norm(target.topics)
    shared_skills = sorted(user_skills & candidate_skills)
    shared_interests = sorted(user_interests & candidate_interests)
    wanted = _norm(source.looking_for)
    candidate_signals = candidate_skills | candidate_interests | _norm(target.looking_for)
    looking_for = sorted(wanted & candidate_signals)
    skill_score = min(100, len(shared_skills) * 20)
    interest_score = min(100, len(shared_interests) * 15)
    looking_score = min(100, len(looking_for) * 25)
    score = round(skill_score * .45 + interest_score * .35 + looking_score * .20)
    reasons = []
    if shared_skills: reasons.append(f"You both work or learn with: {', '.join(shared_skills[:4])}.")
    if shared_interests: reasons.append(f"You share interests: {', '.join(shared_interests[:4])}.")
    if looking_for: reasons.append(f"They match what you are looking for: {', '.join(looking_for[:3])}.")
    return score, reasons, {"skills": skill_score, "interests": interest_score, "looking_for": looking_score, "shared_skills": shared_skills, "shared_interests": shared_interests, "looking_for_matches": looking_for}


def recommendations_for(user, limit=30):
    friend_ids = Friendship.objects.filter(Q(user1=user) | Q(user2=user)).values_list("user1_id", "user2_id")
    blocked = set(UserBlock.objects.filter(Q(blocker=user) | Q(blocked=user)).values_list("blocker_id", flat=True)) | set(UserBlock.objects.filter(Q(blocker=user) | Q(blocked=user)).values_list("blocked_id", flat=True))
    following = set(Follow.objects.filter(follower=user).values_list("following_id", flat=True))
    from django.contrib.auth import get_user_model
    User = get_user_model()
    excluded = {user.id, *blocked, *following}
    for pair in friend_ids:
        excluded.update(pair)
    candidates = User.objects.filter(is_active=True).exclude(id__in=excluded)
    rows = []
    for candidate in candidates[:300]:
        profile = getattr(candidate, "social_profile", None)
        if profile is not None and not profile.discoverable:
            continue
        score, reasons, breakdown = score_candidate(user, candidate)
        if score <= 0:
            continue
        rec, _ = SocialRecommendation.objects.update_or_create(user=user, candidate=candidate, defaults={"score": score, "reasons": reasons, "breakdown": breakdown, "status": "active"})
        rows.append(rec)
    return sorted(rows, key=lambda x: x.score, reverse=True)[:limit]
