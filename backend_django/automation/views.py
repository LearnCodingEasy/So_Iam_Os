# backend_django\automation\views.py
from automation.services.window_service import list_open_windows
from rest_framework.decorators import api_view
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django.db import transaction
from automation.services.program_service import scan_and_store_elements

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
from .serializers import (
    ProgramSerializer,
    ProgramElementSerializer,
    WorkflowSerializer,
    WorkflowNodeSerializer,
    WorkflowEdgeSerializer,
    ActionSerializer,
    TaskSerializer,
    TaskRunSerializer,
    ScreenStateSerializer,
    DelaySerializer,
)
from .engine_runtime import (
    _open_program,
    _close_program,
    _get_program_status,
    run_action_instance,
)
from .workflow_runner import execute_workflow
from .window_manager import focus_window, maximize_window
from django.db.models import Count

# Console
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
console = Console()


@api_view(["GET"])
def get_open_windows(request):
    try:
        data = list_open_windows()
        return Response({
            "success": True,
            "data": data
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
# ==================================================
# 1️⃣ Program
# ==================================================


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def open(self, request, pk=None):
        program = self.get_object()
        result = _open_program(
            program.executable_path,
            program.project_path
        )
        return Response(result)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        program = self.get_object()
        result = _close_program(program.executable_path)
        return Response(result)

    @action(detail=True, methods=["get"])
    def status(self, request, pk=None):
        program = self.get_object()
        return Response(
            _get_program_status(program.executable_path)
        )

    @action(detail=True, methods=['post'])
    def focus(self, request, pk=None):
        program = self.get_object()
        focus_window(program)
        return Response({'status': 'focused'})

    @action(detail=True, methods=['post'])
    def maximize(self, request, pk=None):
        program = self.get_object()
        maximize_window(program)
        return Response({'status': 'maximized'})

    @action(detail=True, methods=["post"])
    def scan_elements(self, request, pk=None):
        program = self.get_object()
        custom_pattern = request.data.get("window_title_pattern", None)

        try:
            created_count = scan_and_store_elements(
                program, request.user, custom_pattern=custom_pattern
            )
        except RuntimeError as e:
            # خطأ من الـ scanner (مثلاً pywinauto مش متثبّت)
            return Response({"error": str(e)}, status=500)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)

        if created_count == 0:
            return Response({
                "status": "warning",
                "message": "مفيش عناصر جديدة — تأكد إن النافذة مفتوحة وغير مصغّرة",
                "count": 0,
            })

        return Response({
            "status": "success",
            "message": f"✅ تم حفظ {created_count} عنصر في الشجرة",
            "count": created_count,
        })


# ==================================================
# 2️⃣ ProgramElement
# ==================================================


class ProgramElementViewSet(viewsets.ModelViewSet):
    queryset = ProgramElement.objects.all()
    serializer_class = ProgramElementSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ==================================================
# 3️⃣ Workflow
# ==================================================


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        workflow = self.get_object()
        if workflow.status != "active":
            return Response(
                {"error": "Workflow is not active"},
                status=400
            )

        task_run = TaskRun.objects.create(
            workflow=workflow,
            status="running",
            created_by=request.user
        )

        execute_workflow(workflow.id, request.user)
        # task_run.status = "success"
        task_run.refresh_from_db()
        task_run.finished_at = timezone.now()
        task_run.save()

        return Response({
            "status": "workflow_executed",
            "task_run_id": task_run.id
        })

    """
    🔗 جلب كل الأحداث المرتبطة بـ 
    Workflow
    محدد
    """

    @action(detail=True, methods=["get"])
    def full_events(self, request, pk=None):
        workflow = self.get_object()

        nodes = []
        edges = []

        # =========================
        # 1️⃣ Nodes
        # =========================
        for node in workflow.nodes.all():
            actions = node.actions.all().order_by("created_at")

            nodes.append({
                "id": str(node.id),
                "type": node.node_type or "default",
                "position": {
                    "x": node.position_x or 0,
                    "y": node.position_y or 0,
                },
                "data": {
                    "label": node.label,
                    "node": WorkflowNodeSerializer(node).data,
                    "actions": ActionSerializer(actions, many=True).data,
                }
            })

        # =========================
        # 2️⃣ Edges
        # =========================
        for edge in workflow.edges.all():
            edges.append({
                "id": str(edge.id),
                "source": str(edge.source_node_id),
                "target": str(edge.target_node_id),
                "type": edge.edge_type or "default",
                "data": {
                    "condition": edge.condition
                }
            })

        # ============================================
        # 🖥 Console Table
        # ============================================

        console.rule("[bold green]Workflow Nodes")

        table = Table(
            title="Workflow Nodes",
            box=box.SIMPLE_HEAVY,
            header_style="bold magenta"
        )

        table.add_column("Node ID", style="green")
        table.add_column("Type", style="cyan")
        table.add_column("Label", style="yellow")
        table.add_column("Position", style="red")

        for n in nodes:
            table.add_row(
                n["id"],
                n["type"],
                n["data"].get("label", ""),
                f"x:{n['position']['x']} y:{n['position']['y']}"
            )

        console.print(table)
        console.rule()

        return Response({
            "nodes": nodes,
            "edges": edges
        })

    @action(detail=True, methods=['post'])
    def save_all(self, request, pk=None):

        workflow = self.get_object()

        nodes_data = request.data.get("nodes", [])
        edges_data = request.data.get("edges", [])

        existing_nodes = {str(n.id): n for n in workflow.nodes.all()}
        existing_edges = {str(e.id): e for e in workflow.edges.all()}

        sent_node_ids = set()
        sent_edge_ids = set()

        # =====================================================
        # 1️⃣ Nodes Sync
        # =====================================================

        for n in nodes_data:

            node_id = str(n.get("id"))
            position = n.get("position", {})
            node_info = n.get("data", {}).get("node", {})

            sent_node_ids.add(node_id)

            if node_id in existing_nodes:

                node = existing_nodes[node_id]

                node.position_x = position.get("x", 0)
                node.position_y = position.get("y", 0)

                node.label = node_info.get("label", node.label)
                node.node_type = node_info.get("node_type", node.node_type)

                node.config = node_info.get("config", node.config)

                node.program_id = node_info.get("program")
                node.element_id = node_info.get("element")

                node.save()

            else:

                WorkflowNode.objects.create(
                    id=node_id,
                    workflow=workflow,
                    position_x=position.get("x", 0),
                    position_y=position.get("y", 0),
                    label=node_info.get("label", ""),
                    node_type=node_info.get("node_type", "custom"),
                    config=node_info.get("config", {}),
                    program_id=node_info.get("program"),
                    element_id=node_info.get("element"),
                    created_by=request.user
                )

        # حذف النود التي لم تعد موجودة
        for node_id, node in existing_nodes.items():
            if node_id not in sent_node_ids:
                node.delete()

        # =====================================================
        # 2️⃣ Edges Sync
        # =====================================================

        for e in edges_data:

            edge_id = str(e.get("id"))
            sent_edge_ids.add(edge_id)

            if edge_id in existing_edges:

                edge = existing_edges[edge_id]

                edge.source_node_id = e.get("source")
                edge.target_node_id = e.get("target")
                edge.condition = e.get("data", {}).get("condition", "success")

                edge.save()

            else:

                WorkflowEdge.objects.create(
                    id=edge_id,
                    workflow=workflow,
                    source_node_id=e.get("source"),
                    target_node_id=e.get("target"),
                    condition=e.get("data", {}).get("condition", "success"),
                    created_by=request.user
                )

        # حذف edges غير الموجودة
        for edge_id, edge in existing_edges.items():
            if edge_id not in sent_edge_ids:
                edge.delete()

        return Response({
            "message": "Workflow synced successfully"
        })


# ==================================================
# 4️⃣ WorkflowNode (VueFlow Node)
# ==================================================


class WorkflowNodeViewSet(viewsets.ModelViewSet):
    queryset = WorkflowNode.objects.all()
    serializer_class = WorkflowNodeSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        """
        ▶️ تشغيل Node واحدة فقط (Debug / Test)
        """
        node = self.get_object()
        results = []

        # جلب كل الـ Actions المرتبطة بالنود
        actions = node.actions.all().order_by("created_at")

        for action_obj in actions:
            result = run_action_instance(
                action_obj,
                node.program
            )
            results.append({
                "action_id": action_obj.id,
                "result": result
            })

        return Response({
            "status": "node_executed",
            "node_id": node.id,
            "results": results
        })

    """
    🔗 جلب كل الأحداث المرتبطة بـ Node محدد
    """

    @action(detail=True, methods=["get"])
    def full_events(self, request, pk=None):
        node = self.get_object()

        # =========================
        # 1️⃣ actions
        # =========================
        actions = node.actions.all().order_by("created_at")

        return Response({
            "node": WorkflowNodeSerializer(node).data,
            "actions": ActionSerializer(actions, many=True).data,
        })


# ==================================================
# 5️⃣ WorkflowEdge
# ==================================================


class WorkflowEdgeViewSet(viewsets.ModelViewSet):
    queryset = WorkflowEdge.objects.all()
    serializer_class = WorkflowEdgeSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user
                        )


# ==================================================
# 6️⃣ Action
# ==================================================

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # Send Created By user Created Program
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # 🔹 تعديل الأكشن
    @action(detail=True, methods=['patch'])
    def update_type(self, request, pk=None):
        action_obj = self.get_object()
        new_type = request.data.get("action_type")
        if new_type:
            action_obj.action_type = new_type
            action_obj.save()
            return Response({"success": True, "action_type": action_obj.action_type})
        return Response({"success": False, "error": "No action_type provided"}, status=400)

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        action = self.get_object()
        result = run_action_instance(
            action,
            action.node.program if action.node else None
        )
        return Response(result)

    # ============================================
    # 🧠 Templates by Program
    # ============================================
    @action(detail=False, methods=["get"])
    def templates_by_program(self, request):
        program_id = request.query_params.get("program")

        if not program_id:
            return Response({"error": "program required"}, status=400)

        actions = (
            Action.objects
            .filter(node__program_id=program_id)
            .values("action_type", "payload")
            .annotate(usage_count=Count("id"))
            .order_by("-usage_count")
        )

        return Response(actions)


# ==================================================
# 7️⃣ Task
# ==================================================


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ==================================================
# 8️⃣ TaskRun
# ==================================================

class TaskRunViewSet(viewsets.ModelViewSet):
    queryset = TaskRun.objects.all().order_by("-started_at")
    serializer_class = TaskRunSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ==================================================
# 9️⃣ ScreenState
# ==================================================
class ScreenStateViewSet(viewsets.ModelViewSet):
    """
    🎥 ScreenState API
    ------------------
    مسؤول عن:
    - حفظ لحظات التركيز أثناء الفيديو
    - تحديد zoom / highlight / arrows
    - ربط الأحداث بزمن الفيديو
    """

    queryset = ScreenState.objects.all()
    # queryset = ScreenState.objects.all().order_by("start_time")
    serializer_class = ScreenStateSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """
        📦 Bulk Create
        -------------
        استقبال مجموعة ScreenStates مرة واحدة
        (مفيد عند استيراد JSON من الأوتوميشن)
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"status": "screen_states_created", "count": len(serializer.data)},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["get"])
    def by_task_run(self, request):
        """
        🔗 Filter by TaskRun
        -------------------
        جلب كل ScreenStates الخاصة بتسجيل معين
        """
        task_run_id = request.query_params.get("task_run")
        if not task_run_id:
            return Response(
                {"error": "task_run parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        states = ScreenState.objects.filter(task_run_id=task_run_id)
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)

# ==================================================
# 🔟 Delay
# ==================================================


class DelayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Delay.objects.all()
    serializer_class = DelaySerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
