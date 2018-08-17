from unittest import mock

import weasyprint

from central.services import exceptions
from pdf_service.base import test
from central.services import html_to_pdf_converter


class BaseHTML2PDFConverterTest(test.BaseSimpleTest):
    pass


class WeEasyPrintHTML2PDFConverterTest(BaseHTML2PDFConverterTest):
    def setUp(self):
        super().setUp()
        self.test_html = """
        <html>
            <body>
                <div style="margin-top: 10px">Hallow, <strong>World!</strong>
                </div>
            </body>
        </html>
        """
        self.service = html_to_pdf_converter.WeEasyPrintHTML2PDFConverter()

    def test_html_to_pdf_convert_success(self):
        result = self.service.convert_html_to_pdf(self.test_html)

        self.assertTrue(result)
        self.assertIsInstance(result, bytes)
        self.assertEqual(b"%PDF", result[:4])

    @mock.patch.object(weasyprint.HTML, 'write_pdf')
    def test_html_to_pdf_convert_raises_if_error_status_was_returned(self, converter_mock):
        converter_mock.side_effect = Exception

        self.assertRaises(
            exceptions.HTML2PDFInvalidConversionException,
            self.service.convert_html_to_pdf,
            self.test_html
        )
