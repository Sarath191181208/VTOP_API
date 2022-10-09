class InvalidCredentialsException(Exception):

    def __init__(self, status_code: int, *args: object) -> None:
        self.status_code = status_code
        self.msg = "Invalid Username (or) Password"
        super().__init__(*args)