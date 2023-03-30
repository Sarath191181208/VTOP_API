from functools import wraps
import logging
from typing import Dict
from flask import jsonify, session

from src.vtop_handler.Exceptions.bad_request import BadRequestException
from src.vtop_handler.Exceptions.custom_base_exception import CustomBaseException


def is_logged_in(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        cookie = session.get("cookie", None)
        if cookie is None:
            return jsonify({"Error": "You must login to access this route! "}), 401
        return await func(*args, **kwargs)
    return wrapper


def may_throw(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomBaseException as exception:
            return jsonify({"Error": exception.msg}), exception.status_code
        except Exception as e:
            logging.exception(e)
            print(e)
            print(e.__traceback__)
            return jsonify({"Error": "Internal Server Error"}), 500
    return wrapper


def raise_if_not_args_passed(request_args: Dict[str, str], *args: str):
    """
    Checks if the request args contains the required args if not 
    raises a BadRequestException
    """
    not_passed_args = [arg for arg in args if arg not in request_args.keys()]
    if len(not_passed_args) > 0:
        raise BadRequestException(
            f"You must provide {', '.join(not_passed_args)} to access this route!")
