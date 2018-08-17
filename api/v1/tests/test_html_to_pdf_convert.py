from unittest import mock
import io

from django.urls import reverse_lazy
from django.test import utils
from rest_framework import status

from central.services import convert_facade
from central.services import exceptions
from pdf_service.base import test


class HTMLToPdfConverterViaLinkV1Test(test.BaseV1TestCase):
    URL = reverse_lazy("v1_convert_html_to_pdf_link")

    def setUp(self):
        super().setUp()
        self.test_response = b'%PDF'
        self.test_url = "https://test.se/test/"

    @mock.patch.object(convert_facade.ConvertFacadeService, 'convert_html_to_pdf_using_link')
    def test_convert_using_link(self, service_mock):
        service_mock.return_value = self.test_response

        response = self.client.post(self.URL, {"url": self.test_url})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_response, response.content)
        self.assertTrue(service_mock.called)

    @mock.patch.object(convert_facade.ConvertFacadeService, 'convert_html_to_pdf_using_link')
    def test_convert_using_link_failed_if_internal_exception_raises(self, service_mock):
        service_mock.side_effect = exceptions.BaseGetHTMLByUrlException

        response = self.client.post(self.URL, {"url": self.test_url})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(service_mock.called)


@utils.override_settings(
    HTML_CHECKER="central.services.html_check.HTMLChecker"
)
class HTMLToPdfConverterViaHtmlDataV1Test(test.BaseV1TestCase):
    URL = reverse_lazy("v1_convert_html_to_pdf_data")

    def setUp(self):
        super().setUp()
        self.test_response = b'%PDF'
        self.test_html = "<html><body>Test</body></html>"

    def _generate_html_file(self, html: str=None, name='test.html') -> io.BytesIO:
        html = html or self.test_html
        file = io.BytesIO()
        file.write(html.encode())
        file.name = name
        file.seek(0)

        return file

    @mock.patch.object(convert_facade.ConvertFacadeService, 'convert_html_to_pdf_using_data')
    def test_convert_using_html_data(self, service_mock):
        service_mock.return_value = self.test_response

        response = self.client.post(self.URL, {"html_file": self._generate_html_file()}, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_response, response.content)
        self.assertTrue(service_mock.called)

    @mock.patch.object(convert_facade.ConvertFacadeService, 'convert_html_to_pdf_using_data')
    def test_convert_using_link_failed_if_internal_exception_raises(self, service_mock):
        service_mock.side_effect = exceptions.HTML2PDFBaseConversionException

        response = self.client.post(self.URL, {"html_file": self._generate_html_file()}, format='multipart')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(service_mock.called)

    @mock.patch.object(convert_facade.ConvertFacadeService, 'convert_html_to_pdf_using_data')
    def test_convert_using_link_failed_if_invalid_html(self, service_mock):
        service_mock.return_value = self.test_response

        response = self.client.post(self.URL, {"html_file": self._generate_html_file(name="file.zip")}, format='multipart')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(service_mock.called)
