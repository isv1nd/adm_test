class ServiceBaseException(Exception):
    message = None

    def __init__(self, message=None, *args, **kwargs):
        message = self.message or message
        super().__init__(message, *args, **kwargs)
