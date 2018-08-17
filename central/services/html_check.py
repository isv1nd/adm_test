import abc
import logging

import bs4

from central.services import exceptions
from pdf_service.base import service


LOG = logging.getLogger(__name__)


class AbstractHTMLChecker(service.BaseService, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check_html(self, html_data: str) -> str:
        pass


class HTMLChecker(AbstractHTMLChecker):
    """This validation is just example. Html validation is a
    little bit more complex process.
    """
    def check_html(self, html_data: str) -> str:
        try:
            html_data = bs4.BeautifulSoup(html_data, "html.parser")
            html_tag = html_data.find("html")
            if not (html_tag and isinstance(html_tag.find_parent(), bs4.BeautifulSoup)):
                raise exceptions.InvalidHTML
            return str(html_data)
        except Exception as exc:
            LOG.info(exc)
            raise exceptions.InvalidHTML

