from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.services.program_service import scan_and_store_elements
from automation.models import Program
from automation.api.serializers import ProgramSerializer
from automation.engine_runtime import _open_program, _close_program, _get_program_status
from automation.window_manager import focus_window, maximize_window


# ==================================================
# 1️⃣ Program
# ==================================================


class ProgramViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return Program.objects.filter(created_by=self.request.user)
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
