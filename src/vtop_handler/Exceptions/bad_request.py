class BadRequestException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self.status_code = 400
        self.msg = msg
        super().__init__(*args)
