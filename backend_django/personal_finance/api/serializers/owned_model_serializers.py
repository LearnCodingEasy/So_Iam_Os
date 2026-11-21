from rest_framework import serializers


class OwnedModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def validate_category(self, category):
        if category is not None and category.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Category does not belong to the current user.")
        return category
