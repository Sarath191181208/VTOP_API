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

import PIL
import json
import base64
from PIL import Image
from bs4 import BeautifulSoup

import aiohttp

from typing import Union
from .constants import VTOP_DO_LOGIN_URL, VTOP_LOGIN_URL, VTOP_BASE_URL, HEADERS

CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)

# opening bitmpas of the characters to compare
curr_dir = os.path.dirname(__file__)
bitmaps_path = os.path.join(curr_dir, 'bitmaps.json')
BITMAPS = json.load(open(bitmaps_path))

def _img_match_percentage(img_char_matrix, char_matrix) -> float:
    """
    This function returns the percentage of matching pixels between two images
    """
    char_width, char_height = CHARACTER_DIM
    match_count = 1
    mismatch_count = 1

    _is_black = lambda val : val == 0
    _is_white = lambda val : val == 255
    # iterating throught the entire image
    for y in range(char_height):
        for x in range(char_width):
            # temp vars to store the pixel values
            _char_pixel = char_matrix[y][x]
            _img_pixel = img_char_matrix[x, y]
            # both char and img pixel match with them being black
            if _is_black(_char_pixel) and _img_pixel == _char_pixel:
                match_count += 1
            # since white is the background, we count it as mismatch
            if _is_white(_img_pixel):
                mismatch_count += 1
    # calculating the percentage of matching pixels
    percent_match = match_count / mismatch_count
    return percent_match 

def _identify_chars(img: PIL.Image)-> str:
    """
    This function identifies and returns the captcha
    """

    img_width, img_height = CAPTCHA_DIM
    char_width, char_height = CHARACTER_DIM

    char_crop_threshold = {'upper': 12, 'lower': 44}
    # helper function to crop the image
    _crop_img = lambda img, x, width : img.crop((x, char_crop_threshold['upper'], x+width, char_crop_threshold['lower']))
        
    captcha =""

    # loop through individual characters
    for i in range(0, img_width, char_width):
        # crop the particular character
        cropped_img = _crop_img(img, x = i, width=char_width).convert('L')
        # loading the image for pixel operations
        img_char_matrix = cropped_img.load()
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

def _solve_captcha(img: PIL.Image) -> Union[str, None]:
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

def _find_captcha(login_html:str) -> Union[str, None]:
    """finds the captcha image in the login page"""

    start_idx = login_html.find('src="data:image/png;base64,')
    if start_idx == -1: # i.e no captcha found
        return None

    # taking the data in the src with the other html data
    alt_text = login_html[start_idx+len('src="') :] 

    # finding where the src quote ends
    end_idx = alt_text.find('"')

    # taking the image data from the src
    captcha_src = alt_text[:end_idx].replace('data:image/png;base64, ', '')
    return captcha_src

def _remove_pixel_noise(img):
    """
    this function removes the one pixel noise in the captcha
    """
    img_width = CAPTCHA_DIM[0]
    img_height = CAPTCHA_DIM[1]

    img_matrix = img.convert('L').load()
    # Remove noise and make image binary
    for y in range(1, img_height - 1):
        for x in range(1, img_width - 1):
            if img_matrix[x, y-1] == 255 and img_matrix[x, y] == 0 and img_matrix[x, y+1] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x-1, y] == 255 and img_matrix[x, y] == 0 and img_matrix[x+1, y] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x, y] != 255 and img_matrix[x, y] != 0:
                img_matrix[x, y] = 255

    return img_matrix

def _str_to_img(src: str) -> PIL.Image:
    # decoding the base64 string i.e string -> bytes -> image
    im = base64.b64decode(src)
    # converting the image to PIL format
    img = PIL.Image.open(io.BytesIO(im))
    return img

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
        captcha_src = _find_captcha(login_html)
        # return if no captcha found
        if captcha_src is None: return (None, None, False)
        # converting the captcha string to a PIL image
        captcha_img = _str_to_img(captcha_src)
        # filtering the noise in the image and converting it to binary
        _remove_pixel_noise(captcha_img)
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
    for _ in range(8):
        username, valid = await generate_session(username, password, sess)
        if valid:
            break
    print(f"{username} is {'valid' if valid else 'invalid'}")
    return username, valid
