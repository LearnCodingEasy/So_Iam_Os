# backend_django\automation\serializers.py


from rest_framework import serializers
from .models import (
    Program,
    ProgramElement,
    Workflow,
    WorkflowNode,
    WorkflowEdge,
    Action,
    Task,
    TaskRun,
    ScreenState,
    Delay,
)


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
# ==================================================
# 3️⃣ Workflow
# ==================================================


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")


# ==================================================
# 6️⃣ Action
# ==================================================

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")

# ==================================================
# 4️⃣ WorkflowNode (VueFlow Node)
# ==================================================


class WorkflowNodeSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(
        source="program.name", read_only=True
    )
    element_name = serializers.CharField(
        source="element.name", read_only=True
    )
    actions = ActionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowNode
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")


# ==================================================
# 5️⃣ WorkflowEdge
# ==================================================

class WorkflowEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowEdge
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")


# ==================================================
# 7️⃣ Task
# ==================================================


class TaskSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(
        source="program.name", read_only=True
    )

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")


# ==================================================
# 8️⃣ TaskRun
# ==================================================

class TaskRunSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(
        source="workflow.name", read_only=True
    )

    class Meta:
        model = TaskRun
        fields = "__all__"
        read_only_fields = ("id", "started_at", "slug",
                            "created_at", "updated_at", "created_by")


# ==================================================
# 9️⃣ ScreenState
# ==================================================

class ScreenStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenState
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")

# ==================================================
# 🔟 Delay
# ==================================================


class DelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delay
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
