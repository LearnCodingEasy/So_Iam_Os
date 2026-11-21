from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from automation.models import Workflow, WorkflowNode, WorkflowEdge, TaskRun
from automation.api.serializers import WorkflowSerializer, WorkflowNodeSerializer, ActionSerializer
from rich.console import Console
from rich.table import Table
from rich import box


console = Console()


# ==================================================
# 3️⃣ Workflow
# ==================================================


class WorkflowViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return Workflow.objects.filter(created_by=self.request.user)
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
            return Response({"error": "Workflow is not active"}, status=400)
        from automation.permission_policy import validate_permissions
        permission_result = validate_permissions(workflow, approved=bool(request.data.get("approve")))
        if not permission_result["allowed"]:
            return Response(permission_result, status=403 if permission_result["status"] == "denied" else 409)

        task_run = TaskRun.objects.create(workflow=workflow, status="running", created_by=request.user)
        from automation.tasks import execute_workflow_task
        async_result = execute_workflow_task.delay(str(workflow.id), str(request.user.id), str(task_run.id))
        return Response({"status": "workflow_queued", "task_run_id": str(task_run.id), "task_id": async_result.id}, status=202)

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
