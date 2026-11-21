from rest_framework import serializers
from automation.models import Delay


# ==================================================
# 🔟 Delay
# ==================================================


class DelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delay
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
