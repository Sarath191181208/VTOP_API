class CustomBaseException(Exception):
    def __init__(self, msg: str, status_code: int, *args: object) -> None:
        self.msg = msg
        self.status_code = status_code
        super().__init__(*args)
