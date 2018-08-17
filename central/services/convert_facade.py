import logging

import bs4
from django.conf import settings
from django.utils import module_loading

from pdf_service.base import service

from central.services import get_html_from_remote


LOG = logging.getLogger(__name__)


class ConvertFacadeService(service.BaseService):
    def __init__(self):
        self.get_html_from_remote_service = get_html_from_remote.GetHtmlFromRemoteService()
        self.html_to_pdf_converter = module_loading.import_string(
            getattr(
                settings,
                "HTML_TO_PDF_CONVERTER_CLASS",
                "central.services.html_to_pdf_converter.WeEasyPrintHTML2PDFConverter"
            )
        )()

    def convert_html_to_pdf_using_link(self, html_link):
        html_data = self.get_html_from_remote_service.get_html(html_link)
        return self._convert_html_to_pdf(html_data)

    def convert_html_to_pdf_using_data(self, html_data):
        return self._convert_html_to_pdf(html_data)

    def _convert_html_to_pdf(self, html_data):
        html_data = str(bs4.BeautifulSoup(html_data, "html.parser"))

        pdf = self.html_to_pdf_converter.convert_html_to_pdf(html_data)
        return pdf
