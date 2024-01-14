class BaseException(Exception):
    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code


def __init__(self, message, status_code):
    self.__class__.__bases__[0]().__init__(message, status_code)


## Check smtp server error
DomainError = type("DomainError", (BaseException,), {"init": __init__})
DomainTimeoutError = type("DomainTimeoutError", (BaseException,), {"init": __init__})
AccountPasswordError = type(
    "AccountPasswordError", (BaseException,), {"init": __init__}
)
