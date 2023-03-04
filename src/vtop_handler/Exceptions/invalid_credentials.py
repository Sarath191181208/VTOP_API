from .custom_base_exception import CustomBaseException
class InvalidCredentialsException(CustomBaseException):

    def __init__(self, status_code: int, *args: object) -> None:
        self.status_code = status_code
        self.msg = "Invalid Username (or) Password"
        super().__init__(self.msg, self.status_code, *args)