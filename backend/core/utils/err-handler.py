import traceback
from django.conf import settings
from rest_framework.views import exception_handler


def err_handler(exc, context):
    # Call DRF's default exception handler first to get standard response
    response = exception_handler(exc, context)

    # If response is None, it means DRF didn't handle the error (uncaught 500 error)
    if response is None:
        error_data = {
            "error": "Internal Server Error",
            "message": str(exc),
            "exception_type": exc.__class__.__name__,
        }

        # Include traceback ONLY in DEBUG mode (never leak tracebacks in production!)
        if settings.DEBUG:
            error_data["traceback"] = traceback.format_exc().splitlines()

        from rest_framework import status
        from rest_framework.response import Response

        return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # For standard DRF errors (like 400, 403, 404), structure the body nicely
    response.data = {
        "error": "Request failed",
        "details": response.data,
    }
    return response