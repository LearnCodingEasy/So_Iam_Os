from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for So_Iam_OS models.

    Prevents system-managed fields from being modified
    through the API.
    """

    class Meta:
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()

        for field_name in (
            "id",
            "created_at",
            "updated_at",
        ):
            if field_name in fields:
                fields[field_name].read_only = True

        return fields
