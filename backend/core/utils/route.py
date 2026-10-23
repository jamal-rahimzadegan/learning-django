from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_404_view(request, exception=None):
    return Response(
        {
            "error": "Not Found",
            "message": "The requested API endpoint was not found on this server.",
            "path": request.path
        },
        status=status.HTTP_404_NOT_FOUND
    )