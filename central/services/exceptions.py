from pdf_service.base import exceptions


class BaseCentralException(exceptions.ServiceBaseException):
    pass


class HTML2PDFBaseConversionException(BaseCentralException):
    pass


class HTML2PDFInvalidConversionException(HTML2PDFBaseConversionException):
    message = "Conversion was not successful"


class HTML2PDFUnexpectedException(HTML2PDFBaseConversionException):
    message = "Unexpected error was occurred during conversion"


class BaseGetHTMLByUrlException(BaseCentralException):
    pass


class GetHTMLByUrlTimeoutException(BaseGetHTMLByUrlException):
    message = "Request for html data got too match time"


class GetHTMLByUrlInvalidStatusException(BaseGetHTMLByUrlException):
    message = "Invalid request status was returned for GET request for HTML"


class GetHTMLByUrlInvalidContentTypeException(BaseGetHTMLByUrlException):
    message = "Invalid Content Type for html resource"


class GetHTMLByUrlInvalidHeadStatusException(BaseGetHTMLByUrlException):
    message = "Invalid request status was returned for HEAD request for HTML"
