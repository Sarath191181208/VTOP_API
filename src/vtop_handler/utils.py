from typing import Union


def find_image(login_html:str) -> Union[str, None]:
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