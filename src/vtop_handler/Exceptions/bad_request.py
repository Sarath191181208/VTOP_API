from .custom_base_exception import CustomBaseException


class BadRequestException(CustomBaseException):
    def __init__(self, msg: str, *args: object) -> None:
        self.status_code = 400
        self.msg = msg
        super().__init__(self.msg, self.status_code, *args)
