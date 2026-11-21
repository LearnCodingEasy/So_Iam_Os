from rest_framework import serializers
from automation.models import ProgramElement


# ==================================================
# 2️⃣ ProgramElement
# ==================================================


class ProgramElementSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    get_image = serializers.SerializerMethodField()

    def get_get_image(self, obj):
        return obj.get_image()

    class Meta:
        model = ProgramElement
        fields = [
            'id', 'slug', 'program', 'program_name',
            # Identity
            'name', 'display_text', 'element_type', 'description',
            # Automation
            'automation_id', 'class_name', 'selector_type', 'selector_value',
            'keyboard_shortcut', 'help_text',
            # Coordinates
            'x_coordinate', 'y_coordinate', 'width', 'height',
            # Hierarchy
            'tree_path', 'depth_level', 'parent_element',
            # State
            'is_visible', 'is_enabled', 'is_clickable', 'is_active',
            # Extra
            'raw_properties', 'stability_score', 'get_image',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('id', 'slug', 'created_at',
                            'updated_at', 'created_by')

    def validate_program(self, value):
        request=self.context.get('request')
        if request and value and value.created_by_id != request.user.id: raise serializers.ValidationError('Program does not belong to the current user.')
        return value
