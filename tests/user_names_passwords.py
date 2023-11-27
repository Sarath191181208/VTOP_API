import os
from typing import Any, List, Tuple, Union
import dotenv

dotenv.load_dotenv()

USERNAME = os.getenv("VTOP_USERNAME_1", "")
PASSWORD = os.getenv("VTOP_PASSWORD_1", "")
VITEEE_USERNAME_1 = os.getenv("VITEEE_USERNAME_1", "")
VITEEE_PASSWORD_1 = os.getenv("VITEEE_PASSWORD_1", "")
FRESHER_USERNAME_1 = os.getenv("FRESHER_USERNAME_1", "")
FRESHER_PASSWORD_1 = os.getenv("FRESHER_PASSWORD_1", "")
VTOP_USERNAME_2 = os.getenv("VTOP_USERNAME_2", "")
VTOP_PASSWORD_2 = os.getenv("VTOP_PASSWORD_2", "")

for i in [
    USERNAME,
    PASSWORD,
    VITEEE_USERNAME_1,
    VITEEE_PASSWORD_1,
    FRESHER_USERNAME_1,
    FRESHER_PASSWORD_1,
    VTOP_USERNAME_2,
    VTOP_PASSWORD_2,
]:
    assert i != "", "Please set the environment variables"

username_password_list: List[Tuple[str, str]] = [
    (USERNAME, PASSWORD),
    (VITEEE_USERNAME_1, VITEEE_PASSWORD_1),
    (FRESHER_USERNAME_1, FRESHER_PASSWORD_1),
    (VTOP_USERNAME_2, VTOP_PASSWORD_2),
]


def merge_username_passwords(
    args: List[Tuple[str, str]],
    extended_args: Union[List[Union[List, Tuple, Any]], None],
) -> List:
    """
    Merge the username and password with the extended args
    if the extended args is None, return the args
    if the extended args is a list, merge with username, password
    if the element of extended args = None, it is excluded
    """
    if extended_args is None:
        return args
    func_args = []
    for i, arg in enumerate(extended_args):
        if arg is None:
            continue
        elif isinstance(arg, tuple) or isinstance(arg, list):
            func_args.append((*args[i], *arg))
        else:
            func_args.append((*args[i], arg))
    return func_args
