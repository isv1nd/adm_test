import abc
import io
import logging

from xhtml2pdf import pisa

from pdf_service.base import service


LOG = logging.getLogger(__name__)


class HTML2PDFBaseConversionException(Exception):
    pass


class HTML2PDFInvalidConversionException(HTML2PDFBaseConversionException):
    pass


class HTML2PDFUnexpectedException(HTML2PDFBaseConversionException):
    pass


class AbstractHTML2PDFConverter(service.BaseService, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert_html_to_pdf(self, html_code: str) -> bytes:
        pass


class PisaHTML2PDFConverter(AbstractHTML2PDFConverter):
    def convert_html_to_pdf(self, html_code: str) -> bytes:
        result = io.BytesIO()
        try:
            pdf = pisa.pisaDocument(
                io.BytesIO(html_code.encode("utf8")),
                result
            )
        except Exception as exc:
            LOG.exception(exc)
            raise HTML2PDFUnexpectedException

        if pdf.err:
            raise HTML2PDFInvalidConversionException

        return result.getvalue()
