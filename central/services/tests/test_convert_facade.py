from unittest import mock

from django.test import utils

from pdf_service.base import test
from central.services import convert_facade


@utils.override_settings(
    GET_HTML_BY_URL_TIMEOUT="central.services.html_to_pdf_converter.WeEasyPrintHTML2PDFConverter",
    HTML_CHECKER="central.services.html_check.HTMLChecker"
)
class GetHtmlFromRemoteService(test.BaseSimpleTest):
    def setUp(self):
        super().setUp()
        self.test_html = "<html><body>Test</body></html>"
        self.test_result = b"%PDF"

    @mock.patch("central.services.html_to_pdf_converter.WeEasyPrintHTML2PDFConverter")
    def test_service_call_with_html_data(self, converter_mock: mock.MagicMock):
        converter_mock.return_value.convert_html_to_pdf.return_value = self.test_result

        service = convert_facade.ConvertFacadeService()

        result = service.convert_html_to_pdf_using_data(self.test_html)

        self.assertEqual(self.test_result, result)
        converter_mock.return_value.convert_html_to_pdf.assert_called_once_with(self.test_html)

    @mock.patch("central.services.html_to_pdf_converter.WeEasyPrintHTML2PDFConverter")
    @mock.patch("central.services.get_html_from_remote.GetHtmlFromRemoteService")
    def test_service_call_with_link(self, get_html_mock: mock.MagicMock, converter_mock: mock.MagicMock):
        test_link = "https://test.se/su/"
        get_html_mock.return_value.get_html.return_value = self.test_html
        converter_mock.return_value.convert_html_to_pdf.return_value = self.test_result

        service = convert_facade.ConvertFacadeService()

        result = service.convert_html_to_pdf_using_link(test_link)

        self.assertEqual(self.test_result, result)
        get_html_mock.return_value.get_html.assert_called_once_with(test_link)
        converter_mock.return_value.convert_html_to_pdf.assert_called_once_with(self.test_html)
