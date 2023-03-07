from typing import Union

from src.vtop_handler.Exceptions.invalid_credentials import InvalidCredentialsException


def throw_if_invalid_username_password(username: Union[str, None], password: Union[str, None]) -> bool:
    """validates if the username and password are valid"""
    if username is None or password is None: 
        raise InvalidCredentialsException(status_code=400)
    if username == "" or password == "":
        raise InvalidCredentialsException(status_code=400)
    if len(username) < 5 or len(password) < 3:
        return False
    return True