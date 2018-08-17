import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import response as resp
from rest_framework import status
from rest_framework.views import exception_handler as exc_handler


LOG = logging.getLogger(__name__)


def format_exceptions(response: resp.Response or None, exc: Exception) -> resp.Response:
    if response:
        return_status = 401 if isinstance(exc, exceptions.NotAuthenticated)\
            else response.status_code

        response.data = {
            "exception_type": type(exc).__name__,
            "errors": response.data,
            "status_code": return_status
        }

        response.status_code = return_status
        return response

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_message = _("Seems like error happened. Please, try again later.")

    LOG.exception(str(exc))

    errors = {
        'detail': error_message
    }
    return resp.Response({
        "exception_type": type(exc).__name__,
        "errors": errors,
        "status_code": status_code
    }, status=status_code)


def exception_handler(exc: Exception, context: dict) -> resp.Response:
    return format_exceptions(exc_handler(exc, context), exc)
