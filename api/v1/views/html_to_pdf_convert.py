import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import views
from rest_framework import request as req
from rest_framework import status
from rest_framework import exceptions
from rest_framework import permissions

from api.v1.serializers import html_to_pdf_convert
from central.services import convert_facade
from central.services import exceptions as ctrl_exceptions


LOG = logging.getLogger(__name__)


class BaseConvertView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.convert_service = convert_facade.ConvertFacadeService()

    @staticmethod
    def _generate_file_response(pdf: bytes) -> HttpResponse:
        response_ = HttpResponse(
            pdf, content_type='application/pdf',
            status=status.HTTP_200_OK
        )
        response_['Content-Disposition'] = \
            'attachment; filename="{}"'.format(settings.PDF_FILENAME)

        return response_


class ConvertHtmlToPdfUsingLinkView(BaseConvertView):
    def post(self, request: req.Request, *args, **kwargs) -> HttpResponse:
        serializer = html_to_pdf_convert.URLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            pdf = self.convert_service.convert_html_to_pdf_using_link(
                serializer.validated_data["url"]
            )
        except ctrl_exceptions.BaseGetHTMLByUrlException:
            raise exceptions.ValidationError(_("Invalid HTML resource."))
        except ctrl_exceptions.HTML2PDFBaseConversionException:
            raise exceptions.ValidationError(_("Conversion to PDF was failed."))

        return self._generate_file_response(pdf)


class ConvertHtmlToPdfUsingHtmlDataView(BaseConvertView):
    def post(self, request: req.Request, *args, **kwargs) -> HttpResponse:
        serializer = html_to_pdf_convert.HtmlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            pdf = self.convert_service.convert_html_to_pdf_using_data(
                serializer.validated_data["html_data"]
            )
        except ctrl_exceptions.HTML2PDFBaseConversionException:
            raise exceptions.ValidationError(_("Conversion to PDF was failed."))

        return self._generate_file_response(pdf)
