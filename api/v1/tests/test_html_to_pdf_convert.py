from unittest import mock

from django.urls import reverse_lazy
from rest_framework import status

from central.services import convert_facade
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
