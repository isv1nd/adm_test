from unittest import mock

from pdf_service.base import test
from central.services import html_to_pdf_converter


class BaseHTML2PDFConverterTest(test.BaseTest):
    pass


class PisaHTML2PDFConverterTest(test.BaseTest):
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
        self.service = html_to_pdf_converter.PisaHTML2PDFConverter()

    def test_html_to_pdf_convert_success(self):
        result = self.service.convert_html_to_pdf(self.test_html)

        self.assertTrue(result)
        self.assertIsInstance(result, bytes)
        self.assertEqual(b"%PDF", result[:4])

    @mock.patch("xhtml2pdf.pisa.pisaDocument")
    def test_html_to_pdf_convert_raises_if_error_status_was_returned(self, converter_mock):
        converter_mock.return_value.err = True

        self.assertRaises(
            html_to_pdf_converter.HTML2PDFInvalidConversionException,
            self.service.convert_html_to_pdf,
            self.test_html
        )

    @mock.patch("xhtml2pdf.pisa.pisaDocument")
    def test_html_to_pdf_convert_raises_if_unexpected_error_raises(self, converter_mock):
        converter_mock.side_effect = Exception("Unexpectedly failed")

        self.assertRaises(
            html_to_pdf_converter.HTML2PDFUnexpectedException,
            self.service.convert_html_to_pdf,
            self.test_html
        )
