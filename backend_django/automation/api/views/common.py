from automation.services.window_service import list_open_windows
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
