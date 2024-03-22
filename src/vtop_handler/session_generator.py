"""
    Solves the captcha and logins into the website 
    this session can be used to extract further data

    Usage:
    ------
    > from vtop_handler.session_generator import get_valid_session
    >
    > async def main():
    >   async with aiohttp.ClientSession() as sess:
    >       session_generator.get_valid_session(username, password, sess)
    >
    > if __name__ == "__main__":
    >   asyncio.run(main())
"""

from bs4 import BeautifulSoup
from typing import Tuple 
import aiohttp

from typing import Union


from .Exceptions.captcha_failure import CaptchaFailure
from .Exceptions.invalid_credentials import InvalidCredentialsException
from .Exceptions.invalid_crsf_token import InvalidCRSFToken 

from .utils import find_image
from .constants import  VTOP_LOGIN_URL, VTOP_BASE_URL, HEADERS, VTOP_PRE_LOGIN, VTOP_LOGIN_PAGE_REDIRECT
from .captcha_solver import solve_captcha

def get_csrf_from_input(html: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    csrf_input = soup.find('input', attrs={'name': '_csrf'})
    if csrf_input is None: 
        return None
    csrf_token = csrf_input.get("value")
    return csrf_token

async def init(sess: aiohttp.ClientSession) -> str | None: 
    _html = await sess.get(VTOP_BASE_URL,headers = HEADERS)
    return get_csrf_from_input(await _html.text())

async def setup(sess: aiohttp.ClientSession, csrf_token: str):
    payload = {
        "_csrf": csrf_token,
        "flag": "VTOP"
    }
    await sess.post(VTOP_PRE_LOGIN, data=payload, headers = HEADERS)

async def page(sess: aiohttp.ClientSession):
    await sess.get(VTOP_LOGIN_PAGE_REDIRECT, headers = HEADERS)

async def get_captcha(sess: aiohttp.ClientSession) -> tuple[str, str | None]:
    # going to the main page without this we will get the following response
    # " You are logged out due to inactivity for more than 15 minutes "
    # getting the login page think of it as clicking the login button
    token = await init(sess)
    if token is None: 
        raise InvalidCRSFToken(status_code=500)
    await setup(sess, token)
    await page(sess)
    async with sess.get(VTOP_LOGIN_URL, headers = HEADERS) as resp:
        login_html = await resp.text()
        captcha = find_image(login_html)
        if captcha is None: 
            return token, None
    return token, captcha

async def generate_session(username:str, password:str, sess:  aiohttp.ClientSession
                           ) -> Tuple[Union[str, None], str]:
    """
        This function generates a session with VTOP. Solves captcha
        
        Parameters :
        -----------
        - username : str 
            Username of the user
        - password : str 
            Password of the user
        - sess : aiohttp.ClientSession
            Session object to make requests

        Returns:
        --------
        - username : str | None
            Username of the user
        - crsf_token : str 
            CSRF token for the session
    """
    crsf_token, captcha_src = await get_captcha(sess)

    if captcha_src is None: 
        raise CaptchaFailure("Captcha can't be given from the server")

    solved_captcha = solve_captcha(captcha_src)

    payload = {
        "_csrf":crsf_token, 
        "username": username,    
        "password": password,
        "captchaStr": solved_captcha
    }
    async with sess.post(VTOP_LOGIN_URL, data = payload, headers = HEADERS) as resp:
        post_login_html = await resp.text()
        soup = BeautifulSoup(post_login_html, 'lxml')
        error_type = soup.find('span', {"class": "text-danger", "role": "alert"})

        if error_type is not None:
            error_text = error_type.text.replace("\n", "").strip()
            if error_text == "Invalid LoginId/Password":
                raise InvalidCredentialsException(401)
            if error_text == "Invalid Captcha":
                raise CaptchaFailure("Captcha can't be solved")

        roll_no_ele = soup.find('span', {"class": "navbar-text text-light small fw-bold"})
        if roll_no_ele is None:
            raise InvalidCredentialsException(401)
        
        roll_no_text = roll_no_ele.text
        crsf_token = get_csrf_from_input(post_login_html)
    
        if crsf_token is None:
            raise InvalidCRSFToken(status_code=500)

        return roll_no_text.split()[0], crsf_token

async def get_valid_session(
    username: str, 
    password: str, 
    sess: aiohttp.ClientSession
    )->Tuple[
        Union[str, None],              # username
        bool]:                         # valid
        

    """
        This function generates a session with VTOP. Solves captcha 
        
        Parameters :
        -----------
        - username : str  
            Username of the user
        - password : str 
            Password of the user
        - sess : aiohttp.ClientSession
            Session object to make requests

        Returns:
        --------
        - username : str | None
            Username of the user
        - valid : bool
            True if the session is valid, False otherwise
    """
    valid = False
    for _ in range(5):
        username, valid = await generate_session(username, password, sess)
        if valid:
            break
    print(f"{username} is {'valid' if valid else 'invalid'}")
    return username, valid
