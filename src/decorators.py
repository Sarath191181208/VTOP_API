from functools import wraps
import logging
from flask import jsonify, session

from src.vtop_handler.Exceptions.custom_base_exception import CustomBaseException


def is_cookie_present(func):
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
