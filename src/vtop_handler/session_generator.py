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
import io
import os

import json
import base64
import numpy as np
from bs4 import BeautifulSoup

import PIL
from PIL import Image

import aiohttp

from typing import Union

from .utils import find_image
from .constants import VTOP_DO_LOGIN_URL, VTOP_LOGIN_URL, VTOP_BASE_URL, HEADERS

CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)

# opening bitmpas of the characters to compare
curr_dir = os.path.dirname(__file__)
bitmaps_path = os.path.join(curr_dir, 'bitmaps.json')
BITMAPS = json.load(open(bitmaps_path))
BITMAPS = {k: np.array(v) for k, v in BITMAPS.items()}

def _img_match_percentage(img_char_matrix: np.ndarray, char_matrix: np.ndarray) -> float:
    """
    This function returns the percentage of matching pixels between two images
    """

    match_count = 1
    mismatch_count = 1

    match_count = np.sum(img_char_matrix == char_matrix)
    w, h = img_char_matrix.shape
    mismatch_count = w*h - match_count

    # calculating the percentage of matching pixels
    percent_match = match_count / mismatch_count
    return percent_match 

def _identify_chars(img: np.ndarray)-> str:
    """
    This function identifies and returns the captcha
    """

    img_width, img_height = CAPTCHA_DIM
    char_width, char_height = CHARACTER_DIM

    up_thresh, low_thresh = 12, 44
    # helper function to crop the image
        
    captcha =""

    # loop through individual characters
    for i in range(0, img_width, char_width):
        img_char_matrix = img[up_thresh:low_thresh, i: i+char_width]
        # caluculating the matching percentage
        matches = {}
        global BITMAPS
        for char, char_matrix in BITMAPS.items():
            perc = _img_match_percentage(img_char_matrix, char_matrix)
            matches.update({perc: char.upper()})
        try:
            captcha += matches[max(matches.keys())]
        except ValueError:
            captcha += "0"
    print(captcha)
    return captcha

def _str_to_img(src: str) -> np.ndarray:
    # decoding the base64 string i.e string -> bytes -> image
    im = base64.b64decode(src)
    img = Image.open(io.BytesIO(im)).convert("L")
    img = np.array(img)
    return img

def _solve_captcha(img: np.ndarray) -> Union[str, None]:
    """solves the captcha and returns the solution if solved else returns None"""

    if img is None:
        print("Captcha not found, returning .... None")
        return None
    captcha = None
    try:
        captcha = _identify_chars(img)
    except Exception as e:
        print(e)
    return captcha

async def generate_session(username:str, password:str, sess:  aiohttp.ClientSession) -> tuple[
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
        - session : requests.Session | None
            Session object with the session
        - username : str | None
            Username of the user
        - valid : bool
            True if the session is valid, False otherwise
    """

    # going to the main page without this we will get the following response
    # " You are logged out due to inactivity for more than 15 minutes "
    await sess.get(VTOP_BASE_URL,headers = HEADERS)
    # getting the login page think of it as clicking the login button
    async with sess.post(VTOP_LOGIN_URL, headers = HEADERS) as resp:
        login_html = await resp.text()
        # login_html = await sess.post(VTOP_LOGIN_URL,headers = HEADERS)
        # finding the captcha image form the login page
        captcha_src = find_image(login_html)
        # return if no captcha found
        if captcha_src is None: return (None, None, False)
        # converting the captcha string to a image
        captcha_img = _str_to_img(captcha_src)
        # solving the captcha
        captcha = _solve_captcha(captcha_img)
        # doing the login
        payload = {
            "uname" : username,
            "passwd" : password,
            "captchaCheck" : captcha
        }
        async with sess.post(VTOP_DO_LOGIN_URL, data = payload, headers = HEADERS) as resp:
            post_login_html = await resp.text()
            valid = True
            
            try:
                soup = BeautifulSoup(post_login_html, 'lxml')
                recaptcha_soup = soup.find_all('div', {"id": "captchaRefresh"})
                username = soup.find('input', {"id": "authorizedIDX"})
                if username is not None:
                    username = username.get('value')
                else:
                    valid = False
            except Exception as e:
                print('logging in failed! with error : ', e)
                valid = False
            finally:
                if(len(recaptcha_soup)>0): # i.e if the captcha isn't solved
                    valid = False
                return (username, valid)

async def get_valid_session(
    username: str, 
    password: str, 
    sess: aiohttp.ClientSession
    )->tuple[
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
