from rest_framework import serializers
from automation.models import Action


# ==================================================
# 6️⃣ Action
# ==================================================

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
