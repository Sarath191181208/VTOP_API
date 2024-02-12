from .custom_base_exception import CustomBaseException

class InvalidCRSFToken(CustomBaseException):
    def __init__(self, status_code: int, *args: object) -> None:
        self.status_code = status_code
        self.msg = "The requested resource didn't contain a valid CRSF Token"
        super().__init__(self.msg, self.status_code, *args)
