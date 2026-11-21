from rest_framework import serializers
from automation.models import Program


# ==================================================
# 1️⃣ Program
# ==================================================

class ProgramSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    get_image = serializers.SerializerMethodField()

    def get_get_image(self, obj):
        return obj.get_image()

    class Meta:
        model = Program
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")

    def get_image_url(self, obj):
        return obj.get_image()
