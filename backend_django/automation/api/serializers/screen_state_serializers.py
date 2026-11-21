from rest_framework import serializers
from automation.models import ScreenState


# ==================================================
# 9️⃣ ScreenState
# ==================================================

class ScreenStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenState
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
