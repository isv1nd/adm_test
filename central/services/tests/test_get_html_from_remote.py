from unittest import mock

import requests

from central.services import exceptions
from pdf_service.base import test
from central.services import get_html_from_remote


@mock.patch.object(requests, 'get')
@mock.patch.object(requests, 'head')
class GetHtmlFromRemoteService(test.BaseTest):
    def setUp(self):
        super().setUp()
        self.test_url = "https://test.tst/wild.php"
        self.test_html = "<html><body>Test</body></html>"
        self.test_headers = {'Content-Type': 'text/html; charset=UTF-8'}
        self.service = get_html_from_remote.GetHtmlFromRemoteService()

    def test_get_html_from_remote_success(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.return_value = self._generate_response(
            200, headers=self.test_headers
        )

        get_mock.return_value = self._generate_response(
            200, headers=self.test_headers, text=self.test_html
        )

        result = self.service.get_html(self.test_url)
        self.assertEqual(self.test_html, result)

    def test_handle_redirect_for_head_request(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.side_effect = [
            self._generate_response(
                301, headers={"Location": self.test_url}
            ),
            self._generate_response(
                200, headers=self.test_headers
            ),
        ]

        get_mock.return_value = self._generate_response(
            200, headers=self.test_headers, text=self.test_html
        )

        result = self.service.get_html(self.test_url)

        self.assertEqual(self.test_html, result)
        self.assertTrue(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_head_request_raises_timeout_error_and_skipped(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.return_value = self._generate_response(
            200, headers=self.test_headers
        )
        get_mock.return_value = self._generate_response(
            200,  headers=self.test_headers, text=self.test_html
        )
        result = self.service.get_html(self.test_url)

        self.assertEqual(self.test_html, result)
        self.assertTrue(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_head_request_raises_if_invalid_content_type(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.return_value = self._generate_response(
            200, headers={}
        )

        self.assertRaises(
            exceptions.GetHTMLByUrlInvalidContentTypeException,
            self.service.get_html, self.test_url
        )
        self.assertFalse(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_head_request_raises_if_invalid_status_code(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.return_value = self._generate_response(
            500, headers=self.test_headers
        )
        self.assertRaises(
            exceptions.GetHTMLByUrlInvalidHeadStatusException,
            self.service.get_html, self.test_url
        )
        self.assertFalse(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_get_request_raises_if_invalid_content_type(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.side_effect = requests.RequestException

        get_mock.return_value = self._generate_response(
            200, headers={"Test": "test"}, text=self.test_html
        )

        self.assertRaises(
            exceptions.GetHTMLByUrlInvalidContentTypeException,
            self.service.get_html, self.test_url
        )
        self.assertTrue(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_get_request_raises_timeout_error_if_request_exception_raises(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.side_effect = requests.RequestException
        get_mock.side_effect = requests.RequestException

        self.assertRaises(
            exceptions.GetHTMLByUrlTimeoutException,
            self.service.get_html, self.test_url
        )
        self.assertTrue(get_mock.called)
        self.assertTrue(head_mock.called)

    def test_get_request_raises_if_invalid_status_code(
            self, head_mock: mock.MagicMock, get_mock: mock.MagicMock
    ):
        head_mock.side_effect = requests.RequestException
        get_mock.return_value = self._generate_response(
            500, headers=self.test_headers
        )
        self.assertRaises(
            exceptions.GetHTMLByUrlInvalidStatusException,
            self.service.get_html, self.test_url
        )
        self.assertTrue(get_mock.called)
        self.assertTrue(head_mock.called)

    @staticmethod
    def _generate_response(status: int, text: str=None, headers: dict=None) -> mock.MagicMock:
        response = mock.MagicMock()
        response.status_code = status
        response.text = text
        response.headers = headers or {}
        return response
