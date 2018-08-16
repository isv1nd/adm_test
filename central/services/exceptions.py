class HTML2PDFBaseConversionException(Exception):
    pass


class HTML2PDFInvalidConversionException(HTML2PDFBaseConversionException):
    pass


class HTML2PDFUnexpectedException(HTML2PDFBaseConversionException):
    pass


class BaseGetHTMLByUrlException(Exception):
    pass


class GetHTMLByUrlTimeoutException(BaseGetHTMLByUrlException):
    pass


class GetHTMLByUrlInvalidStatusException(BaseGetHTMLByUrlException):
    pass


class GetHTMLByUrlInvalidContentTypeException(BaseGetHTMLByUrlException):
    pass


class GetHTMLByUrlInvalidHeadStatusException(BaseGetHTMLByUrlException):
    pass
