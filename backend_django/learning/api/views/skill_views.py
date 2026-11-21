from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.models import Skill
from learning.api.serializers import SkillSerializer


# ===================================================
# Skill
# ===================================================


class SkillViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """
    Skills are global system entities.

    Learners can read them but should not create,
    modify, or delete global skills.
    """

    queryset = Skill.objects.filter(
        is_active=True
    )

    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get(
            "category"
        )

        if category:
            queryset = queryset.filter(
                category=category
            )

        return queryset
