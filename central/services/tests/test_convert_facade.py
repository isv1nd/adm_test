from unittest import mock

from django.test import utils

from pdf_service.base import test
from central.services import convert_facade


@utils.override_settings(
    GET_HTML_BY_URL_TIMEOUT="central.services.html_to_pdf_converter.PisaHTML2PDFConverter"
)
class GetHtmlFromRemoteService(test.BaseTest):
    def test_service_instantiation_raises_if_html_data_and_link_empty(self):
        self.assertRaises(ValueError, convert_facade.ConvertFacadeService)

    def test_service_instantiation_raises_if_html_data_and_link_both_provided(self):
        self.assertRaises(ValueError, convert_facade.ConvertFacadeService, "test", "test")

    @mock.patch("central.services.html_to_pdf_converter.PisaHTML2PDFConverter")
    @mock.patch("central.services.get_html_from_remote.GetHtmlFromRemoteService")
    def test_service_call_with_html_data(self, get_html_mock: mock.MagicMock, converter_mock: mock.MagicMock):
        test_html = "<b>Test</b>"
        test_result = b"%PDF"
        converter_mock.return_value.convert_html_to_pdf.return_value = test_result

        service = convert_facade.ConvertFacadeService(html_data=test_html)

        result = service.convert_html_to_pdf()

        self.assertEqual(test_result, result)
        self.assertFalse(get_html_mock.return_value.get_html.called)
        converter_mock.return_value.convert_html_to_pdf.assert_called_once_with(test_html)

    @mock.patch("central.services.html_to_pdf_converter.PisaHTML2PDFConverter")
    @mock.patch("central.services.get_html_from_remote.GetHtmlFromRemoteService")
    def test_service_call_with_link(self, get_html_mock: mock.MagicMock, converter_mock: mock.MagicMock):
        test_link = "https://test.se/su/"
        test_html = "<b>Test</b>"
        test_result = b"%PDF"
        get_html_mock.return_value.get_html.return_value = test_html
        converter_mock.return_value.convert_html_to_pdf.return_value = test_result

        service = convert_facade.ConvertFacadeService(html_link=test_link)

        result = service.convert_html_to_pdf()

        self.assertEqual(test_result, result)
        get_html_mock.return_value.get_html.assert_called_once_with(test_link)
        converter_mock.return_value.convert_html_to_pdf.assert_called_once_with(test_html)
