import abc
import logging

import weasyprint

from central.services import exceptions
from pdf_service.base import service


LOG = logging.getLogger(__name__)


class AbstractHTML2PDFConverter(service.BaseService, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert_html_to_pdf(self, html_code: str) -> bytes:
        pass


class WeEasyPrintHTML2PDFConverter(AbstractHTML2PDFConverter):
    def convert_html_to_pdf(self, html_code: str) -> bytes:
        try:
            return weasyprint.HTML(string=html_code).write_pdf()
        except Exception as exc:
            LOG.exception(exc)
            raise exceptions.HTML2PDFInvalidConversionException
