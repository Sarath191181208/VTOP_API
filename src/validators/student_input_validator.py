def is_valid_username_password(username: str, password: str) -> bool:
    """validates if the username and password are valid"""
    if username is None or password is None:
        return False
    elif len(username) < 5 or len(password) < 3:
        return False
    return True