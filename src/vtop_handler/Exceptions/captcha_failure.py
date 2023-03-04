from .custom_base_exception import CustomBaseException
class CaptchaFailure(CustomBaseException):
    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        self.status_code = 400
        super().__init__(self.message, self.status_code, *args)

    def __str__(self):
        return self.message