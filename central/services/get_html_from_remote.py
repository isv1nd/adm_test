import logging
import requests

from django.conf import settings

from central.services import exceptions
from pdf_service.base import service


LOG = logging.getLogger(__name__)


class GetHtmlFromRemoteService(service.BaseService):
    SUCCESS_STATUS_200 = 200
    METHOD_NOT_IMPLEMENTED_405 = 405
    REDIRECT_300 = 300
    BAD_REQUEST_400 = 400
    PERMANENT_REDIRECT_301 = 301
    TEMP_REDIRECT_301 = 302

    def __init__(self):
        self.request_timeout = settings.GET_HTML_BY_URL_TIMEOUT
        self.allowed_content_types = settings.ALLOWED_CONTENT_TYPES

    def get_html(self, url: str) -> str:
        self._check_head(url)
        return self._get_html_from_response(url)

    def _check_head(self, url: str) -> None:
        for _ in range(2):
            try:
                response = requests.head(url, timeout=self.request_timeout)
            except requests.RequestException:
                return  # e.g. if head method not implemented

            if response.status_code in (
                    self.PERMANENT_REDIRECT_301,
                    self.TEMP_REDIRECT_301
            ) and response.headers.get('Location'):

                url = response.headers['Location']
                continue

            elif self.SUCCESS_STATUS_200 <= response.status_code < self.REDIRECT_300:
                self._check_headers(response)
                return
            elif response.status_code == self.METHOD_NOT_IMPLEMENTED_405:
                return
            else:
                raise exceptions.GetHTMLByUrlInvalidHeadStatusException

    def _get_html_from_response(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.request_timeout)
        except requests.RequestException as exc:
            LOG.error(exc)
            raise exceptions.GetHTMLByUrlTimeoutException

        if not (self.SUCCESS_STATUS_200 <= response.status_code < self.REDIRECT_300):
            raise exceptions.GetHTMLByUrlInvalidStatusException

        self._check_headers(response)

        return response.text

    def _check_headers(self, response: requests.Response) -> None:
        if not any(content_type in response.headers.get('Content-Type', '') for
                   content_type in self.allowed_content_types):
            raise exceptions.GetHTMLByUrlInvalidContentTypeException
